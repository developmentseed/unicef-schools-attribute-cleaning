import pytest
from pydantic import BaseModel, ValidationError

from unicef_schools_attribute_cleaning.models.Longitude import Longitude


class TestLongitude(BaseModel):
    val: Longitude


def test_latitude():
    TestLongitude(val=0)
    TestLongitude(val=180)
    TestLongitude(val=-180)
    with pytest.raises(ValidationError):
        TestLongitude(val=180.0001)
    with pytest.raises(ValidationError):
        TestLongitude(val=-180.0001)
