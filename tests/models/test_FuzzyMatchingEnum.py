import pytest

from unicef_schools_attribute_cleaning.models.FuzzyMatchingEnum import FuzzyMatchingEnum


class Foo(FuzzyMatchingEnum):
    bar = "Bar"
    fnord = "Fnord"
    etc = "Bar"
    also_fnord = "Fnord"


def test_basic():

    f = Foo["bar"]
    assert f.value == "Bar", repr(f)

    f = Foo["Bar"]
    assert f.value == "Bar", repr(f)

    f = Foo["fnord"]
    assert f.value == "Fnord", repr(f)

    f = Foo["also_fnord"]
    assert f.value == "Fnord", repr(f)


def test_fuzzy():

    f = Foo["fnordling"]
    assert f.value == "Fnord", repr(f)

    with pytest.raises(AttributeError):
        Foo["toofuzzy"]
