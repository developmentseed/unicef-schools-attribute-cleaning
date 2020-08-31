import logging
from io import BytesIO, open
from os import getcwd
from os.path import dirname
from pathlib import Path
from typing import Optional

import diskcache as dc
import geopandas as gp
import responses
from iso3166 import countries
from pytest import fixture

from unicef_schools_attribute_cleaning.geocoding.GADMLoader import (
    GADMLoaderContainer,
    GADMLoaderService,
)

logger = logging.getLogger(__name__)
__tmp_dir: Path = Path(getcwd()).joinpath("tests").joinpath("cache")

logger.info(__tmp_dir)
__disk_cache: Optional[dc.Cache] = None

url = "https://biogeo.ucdavis.edu/data/gadm3.6/gpkg/gadm36_MCO_gpkg.zip"


@fixture(autouse=True, scope="session")
def setup_fixtures():
    global __tmp_dir  # TODO maybe possible to use a parameterized pytest fixture instead of global vars?
    global __disk_cache
    logger.info("setup test fixtures")
    with dc.Cache(directory=str(__tmp_dir), disk_pickle_protocol=4) as disk_cache:
        __disk_cache = disk_cache
        yield
        logger.info("teardown test fixtures")
        __disk_cache.clear()


@responses.activate
def test_gadm_loader_with_cache_hit():
    global __disk_cache
    assert __disk_cache is not None
    path = dirname(__file__)
    with open(file=f"{path}/fixtures/gadm36_MCO_gpkg.zip", mode="rb") as zip_file:
        data = BytesIO(initial_bytes=zip_file.read())
        __disk_cache.set(url, data)
        assert __disk_cache.get(url)
        container = GADMLoaderContainer()
        container.config.set("disk_cache", __disk_cache)
        service: GADMLoaderService = container.service()
        file: BytesIO = service.fetch_gadm_file(country=countries.get("MCO"))
        data = file.read()
        size = len(data)
        assert size == 118784


@responses.activate
def test_gadm_loader_no_cache():
    global __disk_cache
    assert __disk_cache is not None
    __disk_cache.clear()
    path = dirname(__file__)
    with open(file=f"{path}/fixtures/gadm36_MCO_gpkg.zip", mode="rb") as zip_file:
        data = zip_file.read()
        responses.add(responses.GET, url, body=data)
    container = GADMLoaderContainer()
    container.config.set("disk_cache", __disk_cache)
    service: GADMLoaderService = container.service()
    file: BytesIO = service.fetch_gadm_file(country=countries.get("MCO"))
    data = file.read()
    size = len(data)
    assert size == 118784


def test_geodataframe_converter():
    container = GADMLoaderContainer()
    container.config.set("disk_cache", __disk_cache)
    service: GADMLoaderService = container.service()
    file: BytesIO = service.fetch_gadm_file(country=countries.get("MCO"))
    geodf: gp.GeoDataFrame = service.gadm_to_geodataframe(file)
    assert not geodf.empty
