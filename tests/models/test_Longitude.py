import pytest
from pydantic import BaseModel, ValidationError

from unicef_schools_attribute_cleaning.models.Longitude import Longitude


class _Longitude(BaseModel):
    val: Longitude


def test_latitude():
    _Longitude(val=0)
    _Longitude(val=180)
    _Longitude(val=-180)
    with pytest.raises(ValidationError):
        _Longitude(val=180.0001)
    with pytest.raises(ValidationError):
        _Longitude(val=-180.0001)
