import pytest

from unicef_schools_attribute_cleaning.models.CountryCodeAlpha2 import (
    CountryCodeAlpha2,
    country_code_validator,
)


def test_validator():
    code: CountryCodeAlpha2 = "MX"
    country_code_validator(code)
    with pytest.raises(ValueError):
        country_code_validator("ZZ")
