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
    altitude=1000,
    gps_confidence=None,
    date=None,
    num_students=100,
    num_teachers=None,
    connectivity=None,
    type_connectivity=None,
    speed_connectivity=None,
    latency_connectivity=None,
    availability_connectivity=None,
    num_computers=12,
    type_school=None,
    educ_level=None,
    environment=None,
    num_classrooms=None,
    num_sections=None,
    water=None,
    electricity=None,
    num_latrines=None,
    provider="devseed",
    provider_is_private=False,
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
    uuid=None,
)


def test_school_constructor():
    """
    Assert the School constructor basically works.
    """
    School.parse_obj(src_fields)


def test_required_fields():
    """
    Assert that removing a required field is invalid.
    """
    src_missing_fields = src_fields.copy()
    src_missing_fields["provider"] = None  # clear a required field
    with pytest.raises(ValidationError):
        School.parse_obj(src_missing_fields)


def test_enumerated_field():
    src = src_fields.copy()
    src["type_connectivity"] = "2G"  # set enumerated value field to something legit
    School.parse_obj(src)


def test_location_not_null_island():
    """
    Assert that lat,lng of 0,0 is never valid.
    """
    fields = src_fields.copy()
    fields["lat"] = 0.0
    fields["lon"] = 0.0
    with pytest.raises(ValidationError):
        School.parse_obj(fields)


def test_tower_location_not_null_island():
    """
   Assert that tower_latitude, lower_longitude of 0,0 is never valid.
   """
    fields = src_fields.copy()
    fields["tower_latitude"] = 0.0
    fields["tower_longitude"] = 0.0
    with pytest.raises(ValidationError):
        School.parse_obj(fields)


def test_altitude_ok():
    """
    Assert that an impossible altitude is invalid.
    """
    fields = src_fields.copy()
    fields["altitude"] = 9000
    with pytest.raises(ValidationError):
        School.parse_obj(fields)


def test_speed_connectivity():
    """
    Assert that an impossible Internet bandwidth value is invalid.
    """
    fields = src_fields.copy()
    fields["speed_connectivity"] = 99999
    School.parse_obj(fields)

    fields["speed_connectivity"] = 10000000
    School.parse_obj(fields)

    fields["speed_connectivity"] = -100
    with pytest.raises(ValidationError):
        School.parse_obj(fields)

    fields["speed_connectivity"] = 99900000
    with pytest.raises(ValidationError):
        School.parse_obj(fields)


def test_latency_connectivity():
    """
    Assert that an impossible Internet latency value is invalid.
    """
    fields = src_fields.copy()
    fields["latency_connectivity"] = 100  # ms
    School.parse_obj(fields)

    fields["latency_connectivity"] = -100
    with pytest.raises(ValidationError):
        School.parse_obj(fields)

    fields["latency_connectivity"] = 6000
    with pytest.raises(ValidationError):
        School.parse_obj(fields)


def test_country_code():
    """
    Assert that an bad ISO country code is invalid.
    """
    fields = src_fields.copy()
    fields["country_code"] = "MX"  # Mexico
    School.parse_obj(fields)

    fields[
        "country_code"
    ] = "ZY"  # unassigned code per https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#ES
    with pytest.raises(ValidationError):
        School.parse_obj(fields)

    fields["country_code"] = "*(&"
    with pytest.raises(ValidationError):
        School.parse_obj(fields)
