"""
Pandas dataframe support module
"""
import logging
from typing import Optional

import pandas as pd
from pandas import DataFrame, Series
from pydantic import ValidationError

from unicef_schools_attribute_cleaning.models.CountryCodeAlpha2 import CountryCodeAlpha2
from unicef_schools_attribute_cleaning.models.School import School

from .standardize_column_names import standardize_column_names

logger = logging.getLogger(__name__)


def dataframe_cleaner(
    dataframe: DataFrame,
    country_code: CountryCodeAlpha2 = "US",
    is_private: bool = True,
    provider: str = "devseed",
    provider_is_private: bool = True,
) -> DataFrame:
    """
    Return cleaned and validated DataFrame via the School pydantic model.
    """
    df = DataFrame(data=dataframe, copy=True)  # do not modify the source dataframe

    # add user-provided columns. these are organizational knowledge; cannot be discovered easily in the data.
    df["country_code"] = country_code
    df["is_private"] = is_private
    df["provider"] = provider
    df["provider_is_private"] = provider_is_private

    # make the dataframe columns match the School schema.
    df = standardize_column_names(df)

    # shortcut/speedup: coercing lat, lon to numeric (the School validator will also filter these out)
    df = df[pd.to_numeric(df["lat"], errors="coerce").notnull()]
    df = df[pd.to_numeric(df["lon"], errors="coerce").notnull()]

    # apply the Schools pydantic model in pandas filter
    df = df.apply(func=dataframe_filter, axis=1)

    # filter out the None values from previous step
    df = df[df["uuid"].notnull()]

    # fix up the data types in pandas
    df = df.convert_dtypes()

    logger.info(
        f"dataframe cleaning: {len(dataframe)} source rows -> {len(df)} cleaned rows"
    )
    return df


def dataframe_filter(row: Series) -> Optional[Series]:
    """
    Pandas filter for schools data cleaning. Use with DataFrame.apply(func=)
    Note: returns Series of dtype=object so it is recommended to call dataframe.convert_dtypes() or other method of
    restoring correct dtypes in Pandas.

    :param row: pandas series of one school row
    :type row: Series
    :return: validated School record
    :rtype:  Optional[Series]
    """
    try:
        s = School.parse_obj(row.to_dict())
        data = s.dict()
        return Series(data=data, dtype=object)
    except ValidationError as err:
        logging.warning(err)
    return None
