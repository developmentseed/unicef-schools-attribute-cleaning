"""
Enumerated type for categories of schools.
"""
from .FuzzyMatchingEnum import FuzzyMatchingEnum


class SchoolType(FuzzyMatchingEnum):
    """SchoolType enumerated type with fuzzy matching."""

    private = "Private"
    public = "Government"
    government = "Government"
    religious = "Religious"
    Коммунальная_собственность = "Government"  # literally: Communal property
    Собственность_предприятий = "Private"  # literally: Enterprise property
    Собственность_иностранных_физических_лиц_Частная_собственность = "Private"
