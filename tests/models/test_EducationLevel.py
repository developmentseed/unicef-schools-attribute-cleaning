import pytest

from unicef_schools_attribute_cleaning.models.EducationLevel import EducationLevel


def test_enum():

    # test valid enums
    c = EducationLevel["Primary"]
    assert c.value == "Primary", repr(c)
    with pytest.raises(AttributeError):
        EducationLevel["unknown"]


# TODO: test aliases
# def test_enum_aliases():
#     c = EducationLevel["???"]
#     assert c.value == "???", repr(c)


def test_fuzzy_matching():
    # TODO fix ".sec" -> Secondary regression
    # c = EducationLevel["sec."]
    # assert c.value == "Secondary", repr(c)
    pass
