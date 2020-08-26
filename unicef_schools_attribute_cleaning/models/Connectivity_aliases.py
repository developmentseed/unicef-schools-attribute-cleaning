"""
Internet Connectivity aliases. These were observed from the initial set of input data sources.
"""
from functools import lru_cache

from .Connectivity import Connectivity

_aliases = dict(
    dsl=["adsl"],
    fiber=["fibre optic", "fiber optic"],
    shdsl=["shdsl", "xdsl", "shdsl/xdsl"],
    radio=["radio link"],
    satellite=["vsat"],
)


@lru_cache(maxsize=None)
def unpack_connectivity_aliases() -> dict:
    """
    Unpack the known aliases for lookup table of alias_column_name -> schema_column_name.
    :return: lookup table.
    :rtype: dict
    :raises: ValueError if an alias has more than one mapping to a schema column
    """
    # initialize the lookup table with the canonical column names, always map to same name.
    schema_column_names = Connectivity.schema()["properties"].keys()
    result = {k: k for k in schema_column_names}

    # add to the lookup table all the known aliases from School_aliases module
    for (schema_column_name, aliases) in schema_column_names.items():
        for alias_column_name in aliases:
            k = alias_column_name.lower()
            v = schema_column_name.lower()
            if result.get(k) is not None:
                raise ValueError(f"duplicate alias for column name: {k}")
            result[k] = v
    return result
