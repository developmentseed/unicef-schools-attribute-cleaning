"""
Fetch country file from gadm.org (Database of Global Administrative Areas)
https://gadm.org/metadata.html

Example of Dependency Injection:

```python
with TemporaryDirectory() as tmp_dir:
    with dc.Cache(str(tmp_dir)) as disk_cache:
        container = GADMLoaderContainer()
        container.config.set("disk_cache", disk_cache)
        service: GADMLoaderService = container.service()
        stream: BytesIO = service.fetch(country=countries.get("MCO"))
        data = stream.read()
        size = len(data)
        assert size == 118784
```
"""
import logging
from functools import lru_cache
from io import BytesIO
from tempfile import NamedTemporaryFile
from zipfile import ZipFile

import fiona
import geopandas as gp
from dependency_injector import containers, providers
from diskcache import Cache
from iso3166 import Country
from requests import get

logger = logging.getLogger(__name__)


class DiskCacheProvider:
    """
    DI Provider for disk cache
    """

    def __init__(self, disk_cache: Cache):
        """Constructor"""
        self.disk_cache: Cache = disk_cache


class GADMLoaderService:
    """
    DI Service fetch gadm geopackage files from gadm.org. Handles disk caching and unzipping.
    """

    # TODO: refactor url_format with dependency injection? EndPointProvider?
    gadm_version = "3.6"
    url_format = "https://biogeo.ucdavis.edu/data/gadm3.6/gpkg/gadm36_{country_code_alpha3}_gpkg.zip"

    def __init__(self, disk_cache: DiskCacheProvider):
        """Constructor"""
        self.disk_cache = disk_cache.disk_cache

    def fetch_gadm_file(self, country: Country) -> BytesIO:
        """
        Fetch and unzip the GADM file. Zip file data backed by disk cache.
        :param country: iso3166 country
        :return: geopackage file
        """
        country_code_alpha3 = country.alpha3
        url = self.url_format.format(country_code_alpha3=country_code_alpha3)
        cached_file = self.disk_cache.get(url)
        if cached_file is not None:
            logger.info(f"cache hit for: {url}")
            return self._unzip(cached_file)
        logger.info(f"cache miss: fetching {url}")
        response = get(url=url, timeout=10)
        in_memory_file = BytesIO(response.content)
        self.disk_cache.set(url, in_memory_file)
        return self._unzip(in_memory_file)

    @staticmethod
    @lru_cache(maxsize=128)
    def _unzip(zip_file: BytesIO) -> BytesIO:
        """
        Unzip and return an in-memory file e.g. gadm36_MCO_gpkg.zip.
        Te archive is expected to contain 2 files: license.txt and gadm36_{country_code_alpha3}.gpkg.
        :param zip_file:
        :return: unzipped geopackage file
        """
        zip_file: ZipFile = ZipFile(zip_file)
        filenames = zip_file.namelist()
        assert (
            len(filenames) == 2
        ), f"expected 2 files in zip archive, got {len(filenames)}"
        for archive_file in zip_file.namelist():
            if ".gpkg" in archive_file:
                return BytesIO(zip_file.read(archive_file))
        raise RuntimeError(f"missing .gpkg in zip file {repr(zip_file)}")

    @staticmethod
    @lru_cache(maxsize=128)
    def gadm_to_geodataframe(gadm_file: BytesIO) -> gp.GeoDataFrame:
        """
        Helper function for converting gadm geopackage (.gpkg) file to pandas geo dataframe.
        :param gadm_file: gadm data file
        :return: geopandas geodata frame
        """
        logger.info("converting geopackage file...")
        data = gadm_file.read()
        with NamedTemporaryFile(suffix=".gpkg") as tmp_file:
            # pandas and fiona want the .gpkg filename to get which driver to use (so write to temporary file)
            filename = tmp_file.name
            with open(filename, "wb") as filehandle:
                filehandle.write(data)
            layer_names = fiona.listlayers(filename)
            # note: the layers should sort alphabetically, e.g. gadm36_HND_0, gadm36_HND_1, gadm36_HND_2
            # gadm36_HND_2 is the most detailed layer so that's the layer we'll return as GeoDataFrame
            layer_names.sort(reverse=True)
            layer_name = layer_names[0]
            df_gadm = gp.read_file(filename, layer=layer_name)
            return df_gadm


class GADMLoaderContainer(containers.DeclarativeContainer):
    """
    DI Container
    """

    config = providers.Configuration()
    disk_cache = providers.Singleton(DiskCacheProvider, disk_cache=config.disk_cache)
    service = providers.Factory(GADMLoaderService, disk_cache=disk_cache)
