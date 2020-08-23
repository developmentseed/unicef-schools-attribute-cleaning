"""
TODO
"""
import logging

from pandas import Series

from ..models.School import School


def series_to_school(row: Series) -> School:
    """
    TODO
    """
    dict = row.to_dict()
    logging.warning(dict)
    return School.parse_obj(row.to_dict())
