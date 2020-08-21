import pytest
from pydantic import ValidationError

from unicef_schools_attribute_cleaning.models.School import School

"""
Tests the pydantic model models/School.py
"""

# setup the required fields for School model tests
src_fields = dict(
    country_code="US",
    admin0=None,
    admin1=None,
    admin2=None,
    admin3=None,
    admin4=None,
    admin_code=None,
    admin_id=None,
    name="test school",
    address=None,
    address2=None,
    phone_number=None,
    person_contact=None,
    email=None,
    postal_code=None,
    lon=-77.03637,
    lat=38.89511,
    lat_test=90.1,
    altitude=None,
    gps_confidence=None,
    date=None,
    num_students=None,
    num_teachers=None,
    connectivity=None,
    type_connectivity=None,
    speed_connectivity=None,
    latency_connectivity=None,
    availability_connectivity=None,
    num_computers=None,
    type_school=None,
    educ_level=None,
    environment=None,
    num_classrooms=None,
    num_sections=None,
    water=None,
    electricity=None,
    num_latrines=None,
    provider=None,
    description=None,
    last_update=None,
    tower_dist=None,
    tower_type_service=None,
    tower_type=None,
    tower_code=None,
    tower_latitude=None,
    tower_longitude=None,
    owner="pydantic",
    is_private=False,
    provider_is_private=False,
    uuid=None,
)


def test_school_constructor():
    School.parse_obj(src_fields)


def test_required_fields():
    src_missing_fields = src_fields.copy()
    src_missing_fields["owner"] = None  # clear a required field
    with pytest.raises(ValidationError):
        School.parse_obj(src_missing_fields)


def test_location_not_null_island():
    assert False


def test_tower_location_not_null_island():
    assert False


def test_gps_confidence_percentage():
    assert False


def test_altitude_ok():
    assert False


def test_speed_connectivity():
    assert False


def test_latency_connectivity():
    assert False


def availability_connectivity():
    assert False
