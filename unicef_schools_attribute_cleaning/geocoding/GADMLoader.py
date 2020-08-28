"""
Fetch country file from gadm.org
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
from zipfile import ZipFile

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

    # TODO: refactor url_format as EndPointProvider?
    url_format = "https://biogeo.ucdavis.edu/data/gadm3.6/gpkg/gadm36_{country_code_alpha3}_gpkg.zip"

    def __init__(self, disk_cache: DiskCacheProvider):
        """Constructor"""
        self.disk_cache = disk_cache.disk_cache

    @classmethod
    @lru_cache(maxsize=128)
    def unzip(cls, zip_file: BytesIO) -> BytesIO:
        """
        Unzip and read a file e.g. gadm36_MCO_gpkg.zip
        """
        zip: ZipFile = ZipFile(zip_file)
        # the archive is expected to contain 2 files: license.txt and gadm36_{country_code_alpha3}.gpkg
        filenames = zip.namelist()
        assert (
            len(filenames) == 2
        ), f"expected 2 files in zip archive, got {len(filenames)}"
        for archive_file in zip.namelist():
            if ".gpkg" in archive_file:
                return BytesIO(zip.read(archive_file))
        raise RuntimeError(f"missing .gpkg in zip file {repr(zip_file)}")

    def fetch(self, country: Country) -> BytesIO:
        """
        Fetch and unzip the GADM file, backed my disk cache.
        """
        country_code_alpha3 = country.alpha3
        url = self.url_format.format(country_code_alpha3=country_code_alpha3)
        cached_file = self.disk_cache.get(url)
        if cached_file is not None:
            logger.info(f"cache hit for: {url}")
            return self.unzip(cached_file)
        logger.info(f"cache miss: fetching {url}")
        response = get(url=url)
        in_memory_file = BytesIO(response.content)
        self.disk_cache.set(url, in_memory_file)
        return self.unzip(in_memory_file)


class GADMLoaderContainer(containers.DeclarativeContainer):
    """
    DI Container
    """

    config = providers.Configuration()

    disk_cache = providers.Singleton(DiskCacheProvider, disk_cache=config.disk_cache)
    service = providers.Factory(GADMLoaderService, disk_cache=disk_cache)
