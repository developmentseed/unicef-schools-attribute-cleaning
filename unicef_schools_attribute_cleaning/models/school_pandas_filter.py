"""
module
"""
import logging
from typing import Optional

from pandas import Series
from pydantic import ValidationError

from .School import School


def school_pandas_filter(row: Series) -> Optional[Series]:
    """
    Pandas filter for schools data cleaning.

    :param row: pandas series of one school row
    :type row: Series
    :return: validated School record
    :rtype:  Optional[Series]
    """
    try:
        s = School.parse_obj(row.to_dict())
        data = s.dict()
        return Series(data=data)
    except ValidationError as err:
        logging.warning(err)
    return None
