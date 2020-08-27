"""
Reverse geocoding to GADM
"""
from typing import Tuple

from shapely.geometry import Point

from ..models.CountryCodeAlpha2 import CountryCodeAlpha2


def point_to_gadm(country_code: CountryCodeAlpha2, location: Point) -> Tuple[str]:
    """TODO"""
    pass
