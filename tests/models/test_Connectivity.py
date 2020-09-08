import pytest

from unicef_schools_attribute_cleaning.models.Connectivity import Connectivity


def test_enum():

    # test valid enums
    c = Connectivity["4G"]
    assert c.value == "4G", repr(c)
    with pytest.raises(AttributeError):
        Connectivity["unknown"]


def test_enum_aliases():
    # LTE is aliases to 4G
    c = Connectivity["LTE"]
    assert c.value == "4G", repr(c)


def test_fuzzy_matching():
    c = Connectivity["FiBrE"]
    assert c.value == "Fiber", repr(c)
