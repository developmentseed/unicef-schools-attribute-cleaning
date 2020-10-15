"""
Utilities for converting between source column names and School schema column names.
"""
import logging
from enum import Enum
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


class MatchType(Enum):
    """Column name Match Type enumerated type."""

    Exact = "Exact"
    Fuzzy = "Fuzzy"


def add_uuid(dataframe: DataFrame):
    """
    Modify in place DataFrame with uuid column added (if not already having uuid column.
    :param dataframe: pandas dataframe (inplace)
    """
    if "uuid" not in dataframe.columns:
        logger.info("uuid column not found, generating uuid4")
        dataframe["uuid"] = dataframe.apply(lambda row: str(uuid4()), axis=1)


@lru_cache(maxsize=128)
def school_schema_column_names() -> List[str]:
    """
    Fetch list of column names from the School model.
    :return: list of column names
    """
    return School.schema()["properties"].keys()


@lru_cache(maxsize=128)
def _unpack_school_column_aliases() -> Dict[str, List[str]]:
    """
    Unpack the known aliases for lookup table of alias_column_name -> schema_column_name.
    :return: lookup table.
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
    dataframe: DataFrame, inplace=True, fuzzy_score_cutoff=90
) -> (DataFrame, str):
    """
    Modify DataFrame's columns to match the School schema. For example can be run
    before instantiating the School model for each DataFrame row.
    :param dataframe: input pandas datafame to modify
    :param inplace: modify in place
    :param fuzzy_score_cutoff: minimum score for fuzzy matching
    :return: new dataframe or modified dataframe
    """
    # TODO: fix inplace below
    df = dataframe
    add_uuid(df)
    schema_column_names = school_schema_column_names()
    alias_lookup = _unpack_school_column_aliases()
    column_mapping = dict()  # src column name -> (schema_col_name, match_type, reason)
    schema_cols_mapped = (
        dict()
    )  # schema column name -> (src_col_name, match_type, reason)
    columns_to_remove = list()
    all_choices = list(schema_column_names) + list(alias_lookup.keys())
    # logger.info(f"all fuzzy choices {pformat(all_choices)}")

    # 1st: search for exact matched on column names
    for src_col_name in df.columns:
        if src_col_name in schema_column_names:
            schema_column_name = src_col_name
            reason = "reason: exact match on column name"
            match_type = MatchType.Exact
            column_mapping[src_col_name] = (schema_column_name, match_type, reason)
            schema_cols_mapped[schema_column_name] = (src_col_name, match_type, reason)

    # 2nd search exact matches on column aliases
    for src_col_name in df.columns:
        if src_col_name in column_mapping:
            continue
        schema_column_name = alias_lookup.get(src_col_name.lower())
        if (
            schema_column_name is not None
            and schema_column_name not in schema_cols_mapped
        ):
            match_type = MatchType.Exact
            assert schema_column_name != src_col_name
            reason = "reason: exact match on column alias"
            column_mapping[src_col_name] = (schema_column_name, match_type, reason)
            schema_cols_mapped[schema_column_name] = (src_col_name, match_type, reason)

    # 3nd: search for fuzzy match on column names and column aliases
    for src_col_name in df.columns:
        if src_col_name in column_mapping:
            continue
        match = process.extractOne(
            src_col_name, all_choices, score_cutoff=fuzzy_score_cutoff
        )
        if match is not None:
            (hit, score) = match
            if hit in schema_column_names:
                schema_column_name = hit
            else:
                schema_column_name = alias_lookup[hit]
            assert schema_column_name in schema_column_names
            if schema_column_name in schema_cols_mapped:
                pass
            else:
                if hit == schema_column_name:
                    reason = f"fuzzy match on column name: {hit} {score}%"
                else:
                    reason = f"fuzzy match on alias column: {hit} {score}%"
                match_type = MatchType.Fuzzy
                column_mapping[src_col_name] = (schema_column_name, match_type, reason)
                schema_cols_mapped[schema_column_name] = (
                    src_col_name,
                    match_type,
                    reason,
                )

    # process renames
    if column_mapping:
        df_col_mapping = {k: v for k, (v, _, _) in column_mapping.items() if k != v}
        logger.info(f"renaming columns: {pformat(df_col_mapping)}")
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
    columns_descr = "\n".join(columns_to_remove)
    columns_removed_report = f"{len(columns_to_remove)} columns removed (not in School schema):\n{columns_descr}"
    return df, columns_removed_report
