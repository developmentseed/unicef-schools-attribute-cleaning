"""
Pandas dataframe support module
"""
import logging
import os
from typing import Optional

import pandas as pd
from diskcache import Cache
from iso3166 import Country
from pandas import DataFrame, Series
from pydantic import ValidationError
from shapely.geometry import Point

from unicef_schools_attribute_cleaning.geocoding.GADMLoader import (
    GADMLoaderContainer,
    GADMLoaderService,
)
from unicef_schools_attribute_cleaning.models.School import Latitude, Longitude, School

from .standardize_column_names import standardize_column_names

logger = logging.getLogger(__name__)


def dataframe_cleaner(
    dataframe: DataFrame,
    country: Country,
    is_private: bool = True,
    provider: str = "devseed",
    provider_is_private: bool = True,
) -> DataFrame:
    """
    Return cleaned and validated DataFrame via the School pydantic model.
    :param pandas dataframe:
    :param country: iso3166 country instance
    :param is_private: organizational knowledge
    :param provider: organizational knowledge
    :param provider_is_private: organizational knowledge
    :return: pandas dataframe with results of cleaning
    :raises: RuntimeError if no records pass validation
    """
    logger.info("copying dataframe...")
    df = DataFrame(data=dataframe, copy=True)  # do not modify the source dataframe

    logger.info("standardizing column names...")

    # add user-provided columns. these are organizational knowledge; cannot be discovered easily in the data.
    # so set them from the function parameters.
    df["country_code"] = country.alpha2
    df["is_private"] = is_private
    df["provider"] = provider
    df["provider_is_private"] = provider_is_private

    # make the dataframe columns match the School schema.
    df = standardize_column_names(df)

    logger.info("filtering rows missing lat,lon...")

    # shortcut/speedup: coercing lat, lon to numeric (the School validator will also filter these out)
    df = df[pd.to_numeric(df["lat"], errors="coerce").notnull()]
    df = df[pd.to_numeric(df["lon"], errors="coerce").notnull()]

    # apply the Schools pydantic model in pandas filter
    logger.info("validating each school row to the schema...")

    df = df.apply(func=_dataframe_filter, axis=1)
    if not isinstance(df, DataFrame):
        # if nothing passes the filter, pandas says the dataframe is instead a Series.
        raise RuntimeError(
            "No records passed School validation model, cannot continue, stopping cleaner."
        )

    # filter out the None values from previous steps: rows not passing School filter(s)
    df = df[df["uuid"].notnull()]

    # fill in administrative areas
    logger.info("lookup GADM areas by lat,lon...")
    _fix_gadm_data(dataframe=df, country=country)

    # filter out the None values from previous step: rows not passing GADM lookup
    # this is disabled because a warning is printed instead. the GADM boundaries may not be detailed enough to discern
    # some border areas, e.g. Zimbabwe vs. Mozambique
    # df = df[df["uuid"].notnull()]

    # fix up the data types in pandas, otherwise many columns will be object types.
    logger.info("readying pandas data types...")
    df = df.convert_dtypes()

    logger.info(f"{len(dataframe)} source rows -> {len(df)} cleaned rows")
    return df


def _fix_gadm_data(dataframe: DataFrame, country: Country):
    cache_dir = os.getcwd()
    disk_cache = Cache(
        cache_dir
    )  # note: not deleting this resource, to allow cache to persist after script finishes.
    container = GADMLoaderContainer()
    container.config.set("disk_cache", disk_cache)
    gadm_service: GADMLoaderService = container.service()
    gadm_file = gadm_service.fetch_gadm_file(country)
    geo_df = gadm_service.gadm_to_geodataframe(gadm_file)

    def gadm_lookup(row: Series) -> Series:
        lat = row["lat"]
        lon = row["lon"]
        point = Point(lon, lat)
        contains_point = geo_df["geometry"].apply(lambda geom: point.within(geom))
        df_match = geo_df[contains_point]
        if len(df_match) == 1:
            return df_match.squeeze()
        else:
            name: str = row["name"]
            uuid: str = row["uuid"]
            lat: Latitude = row["lat"]
            lon: Longitude = row["lon"]
            link: str = _osm_link(lat=lat, lon=lon)
            logger.warning(
                f"school outside of GADM boundaries name={name}, lat,lng={lat},{lon} {link} (uuid={uuid})"
            )
            return pd.Series()

    logger.info("processing each lat,lon...")
    gadm_lookup_df: DataFrame = dataframe.apply(gadm_lookup, axis=1)
    assert isinstance(gadm_lookup_df, DataFrame)  # pandas will sometimes make a Series
    for level in [0, 1, 2, 3, 4]:
        gadm_col = f"NAME_{level}"
        if gadm_col in gadm_lookup_df:
            dataframe[f"admin{level}"] = gadm_lookup_df[gadm_col]
            dataframe["admin_code"] = gadm_lookup_df[f"GID_{level}"]
            dataframe["admin_id"] = gadm_lookup_df[f"GID_{level}"].apply(
                lambda gid: f"{gadm_service.gadm_version},{country.alpha3},GID_{level}={gid}"
            )
    return dataframe


def _dataframe_filter(row: Series) -> Optional[Series]:
    """
    Pandas filter for schools data cleaning. Use with DataFrame.apply(func=)
    Note: returns Series of dtype=object so it is recommended to call dataframe.convert_dtypes() or other method of
    restoring correct dtypes in Pandas.

    :param row: pandas series of one school row
    :return: validated School record
    """
    try:
        s = School.parse_obj(row.to_dict())
        data = s.dict()
        return Series(data=data, dtype=object)
    except ValidationError as err:
        logger.warning(err)
    return None


def _osm_link(lat: Latitude, lon: Longitude) -> str:
    return f"https://www.openstreetmap.org/#map=18/{lat}/{lon}"
