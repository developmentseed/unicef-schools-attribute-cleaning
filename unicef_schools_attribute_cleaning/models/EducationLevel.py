"""
Enumerated type for education level.
"""
from .FuzzyMatchingEnum import FuzzyMatchingEnum


class EducationLevel(FuzzyMatchingEnum):
    """
    EducationLevel enumerated type with fuzzy matching.
    """

    pre_básica = "Pre-Primary"
    primary = "Primary"
    básica = "Primary"
    secondary = "Secondary"
