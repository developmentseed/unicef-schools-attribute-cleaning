"""
Type definition for ISO3166 2 character Country Code
https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes
"""
from typing import Type

from iso3166 import countries
from pydantic import constr

"""
Type CountryCodeAlpha2 (ISO3166 2 character Country Code)
"""
CountryCodeAlpha2: Type[str] = constr(min_length=2, max_length=2)


def country_code_validator(code: CountryCodeAlpha2):
    """
    Pre-process and validate country codes. ISO 3166-1 defines two-letter, three-letter, and three-digit country
    codes.
    :param code: ISO3166 2 character Country Code
    :return: ISO3166 2 character Country Code
    :raises: ValueError
    """
    try:
        c = countries.get(code)
        return c.alpha2
    except KeyError:
        pass
    raise ValueError(f"invalid country, expected ISO 3166 code, got {code}")
