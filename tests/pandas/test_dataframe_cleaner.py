from math import isclose

from shapely.geometry import Point, Polygon

from unicef_schools_attribute_cleaning.pandas.dataframe_cleaner import (
    BUFFER_KM,
    _buffer_for_latitude,
)


def test_buffer_at_equator():
    """At the equator, the distance between a degree of longitude is 68.703 miles (110.567 kilometers)."""
    lat = 0
    lon = 100
    point = Point(lon, lat)
    (buffer_degrees, polygon) = _buffer_for_latitude(point)
    assert isinstance(polygon, Polygon)
    assert isclose(buffer_degrees, BUFFER_KM / 110.567, abs_tol=0.001)


def test_buffer_at_lat40():
    """At 40 degrees north or south, the distance between a degree of longitude is 53 miles (85 kilometers). """
    lat = 40
    lon = 0
    point = Point(lon, lat)
    (buffer_degrees, polygon) = _buffer_for_latitude(point)
    assert isinstance(polygon, Polygon)
    assert isclose(buffer_degrees, BUFFER_KM / 85.0, abs_tol=0.001)
