"""
Enumerated type for education level.
"""
from .FuzzyMatchingEnum import FuzzyMatchingEnum


class EducationLevel(FuzzyMatchingEnum):
    """
    EducationLevel enumerated type with fuzzy matching.
    """

    primary = "Primary"
    secondary = "Secondary"
