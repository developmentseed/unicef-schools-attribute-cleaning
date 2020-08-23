import pytest
from pydantic import BaseModel, ValidationError

from unicef_schools_attribute_cleaning.models.Latitude import Latitude


class _Latitude(BaseModel):
    val: Latitude


def test_latitude():
    _Latitude(val=0)
    _Latitude(val=90)
    _Latitude(val=-90)
    with pytest.raises(ValidationError):
        _Latitude(val=90.0001)
    with pytest.raises(ValidationError):
        _Latitude(val=-90.0001)
