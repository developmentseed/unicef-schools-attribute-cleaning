"""
Utilities for converting between source column names and School schema column names.
"""
import logging
from functools import lru_cache
from pprint import pformat
from typing import Dict, List
from uuid import uuid4

from fuzzywuzzy import process
from pandas import DataFrame

from unicef_schools_attribute_cleaning.models.School import School
from unicef_schools_attribute_cleaning.models.School_aliases import School_aliases

logger = logging.getLogger(__name__)

uuid_column = "uuid"


def add_uuid(dataframe: DataFrame):
    """Modify in place DataFrame with uuid column added (if not already having uuid column)"""
    if "uuid" not in dataframe.columns:
        logger.info("uuid column not found, generating uuid4")
        dataframe["uuid"] = dataframe.apply(lambda row: str(uuid4()), axis=1)


@lru_cache()
def school_schema_column_names() -> List[str]:
    """Fetch list of column names from the School model."""
    return School.schema()["properties"].keys()


@lru_cache()
def _unpack_school_column_aliases() -> Dict[str, List[str]]:
    """
    Unpack the known aliases for lookup table of alias_column_name -> schema_column_name.
    :return: lookup table.
    :rtype: dict
    :raises: ValueError if an alias has more than one mapping to a schema column
    """
    result = dict()
    # add to the lookup table all the known aliases from School_aliases module
    for (schema_column_name, aliases) in School_aliases.items():
        for alias_column_name in aliases:
            k = alias_column_name.lower()
            v = schema_column_name.lower()
            if result.get(k) is not None:
                raise ValueError(f"duplicate alias {v} for column name: {k}")
            result[k] = v
    return result


def standardize_column_names(
    dataframe: DataFrame, inplace=True, fuzzy=True, fuzzy_score_cutoff=90
) -> DataFrame:
    """
    Modify DataFrame's columns to match the School schema. For example can be run
    before instantiating the School model for each DataFrame row.

    - rename columns based upon "manual fix" column aliases (School_aliases module)
    - rename columns based on fuzzy matching
    - drop unknown columns
    - add missing columns
    """
    # logger.info(f"dataframe has columns: {pformat(df.columns)}")
    df = dataframe
    add_uuid(df)
    schema_column_names = school_schema_column_names()
    alias_lookup = _unpack_school_column_aliases()
    column_mapping = dict()
    columns_to_remove = list()
    all_choices = list(schema_column_names) + list(alias_lookup.keys())
    # logger.info(f"all fuzzy choices {pformat(all_choices)}")

    # search for column aliases
    for src_col_name in df.columns:
        # exact match
        schema_column_name = alias_lookup.get(src_col_name.lower())
        if schema_column_name is not None:
            # add to column mappings
            if schema_column_name != src_col_name:
                column_mapping[src_col_name] = (schema_column_name, "alias exact match")
        # fuzzy match
        else:
            match = process.extractOne(
                src_col_name, all_choices, score_cutoff=fuzzy_score_cutoff
            )
            if match is not None:
                (hit, score) = match
                if hit in schema_column_names:
                    schema_column_name = hit
                    reason = f"fuzzy match {score}%"
                else:
                    schema_column_name = alias_lookup[hit]
                    reason = f"fuzzy match on alias column: {hit} {score}%"
                if schema_column_name != src_col_name:
                    column_mapping[src_col_name] = (schema_column_name, reason)

    # process renames
    if column_mapping:
        logger.info(f"renaming columns: {pformat(column_mapping)}")
        df_col_mapping = {
            k: v for k, (v, _) in column_mapping.items()
        }  # _ was the reason (exact match or % match)
        df.rename(columns=df_col_mapping, inplace=inplace)

    # process additions
    columns_to_add = [c for c in schema_column_names if c not in df.columns]
    if columns_to_add:
        logger.info(
            f"adding {len(columns_to_add)} columns from schema: {pformat(columns_to_add)}"
        )
        for schema_col in columns_to_add:
            df[
                schema_col
            ] = None  # this is sloppy to assign None. but OK assuming the dataframe is object type.

    # process removals
    columns_to_remove = [c for c in df.columns if c not in schema_column_names]
    if columns_to_remove:
        logger.info(
            f"removing columns: {pformat(columns_to_remove)} (not in School schema)"
        )
        df.drop(columns=columns_to_remove, inplace=inplace)

    return df
