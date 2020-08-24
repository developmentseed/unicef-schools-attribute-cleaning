"""
1. Use known column aliases from ../models/School_aliases to rename columns.
2. Uses fuzzy matching to select source columns we are using and match them with the column names
in the output schema.
"""
import logging
from functools import lru_cache

from pandas import DataFrame

from unicef_schools_attribute_cleaning.models.School import School
from unicef_schools_attribute_cleaning.models.School_aliases import School_aliases


@lru_cache(maxsize=None)
def _unpack_lookup_aliases() -> dict:
    """
    Unpack the known aliases for lookup table of alias_column_name -> schema_column_name.
    :return: lookup table.
    :rtype: dict
    :raises: ValueError if an alias has more than one mapping to a schema column
    """
    logging.warning("_unpack_lookup_aliases!")

    # initialize the lookup table with the canonical column names, always map to same name.
    schema_column_names = School.schema()["properties"].keys()
    result = {k: k for k in schema_column_names}

    # add to the lookup table all the known aliases from School_aliases module
    for (schema_column_name, aliases) in School_aliases.items():
        for alias_column_name in aliases:
            k = alias_column_name.lower()
            v = schema_column_name.lower()
            if result.get(k) is not None:
                raise ValueError(f"duplicate alias for column name: {k}")
            result[k] = v
    return result


def standardize_column_names(df: DataFrame, inplace=True) -> DataFrame:
    """
    Modify in place DataFrame by renaming columns.
    :param df:
    :type df: DataFrame
    :return: df with standardized column names
    :rtype: DataFrame
    """
    alias_lookup = _unpack_lookup_aliases()
    column_mapping = dict()
    for src_column_name in df.columns:
        schema_column_name = alias_lookup.get(src_column_name.lower())
        if schema_column_name is not None:
            if schema_column_name != src_column_name:
                logging.warning(
                    f"renaming {src_column_name} to {schema_column_name} (known alias)"
                )
            column_mapping[src_column_name] = schema_column_name
    if column_mapping:
        df.rename(columns=column_mapping, inplace=inplace)
    return df
