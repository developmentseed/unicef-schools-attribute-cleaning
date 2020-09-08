import pytest
from pydantic import BaseModel, ValidationError

from unicef_schools_attribute_cleaning.models.Percentage import Percentage


class _Percentage(BaseModel):
    val: Percentage


def test_percentage():
    _Percentage(val=0)
    _Percentage(val=100)
    with pytest.raises(ValidationError):
        _Percentage(val=-1)
    with pytest.raises(ValidationError):
        _Percentage(val=-101.0)
