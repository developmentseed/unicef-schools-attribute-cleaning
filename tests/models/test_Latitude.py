import pytest
from pydantic import BaseModel, ValidationError

from unicef_schools_attribute_cleaning.models.Latitude import Latitude


class TestLatitude(BaseModel):
    val: Latitude


def test_latitude():
    TestLatitude(val=0)
    TestLatitude(val=90)
    TestLatitude(val=-90)
    with pytest.raises(ValidationError):
        TestLatitude(val=90.0001)
    with pytest.raises(ValidationError):
        TestLatitude(val=-90.0001)
