"""
Enumerated type for categories of schools.
"""
from .FuzzyMatchingEnum import FuzzyMatchingEnum


class SchoolType(FuzzyMatchingEnum):
    """SchoolType enumerated type with fuzzy matching."""

    private = "Private"
    government = "Government"
    religious = "Religious"
