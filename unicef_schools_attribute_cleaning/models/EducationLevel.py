"""
Enumerated type for education level.
"""
from .FuzzyMatchingEnum import FuzzyMatchingEnum


class EducationLevel(FuzzyMatchingEnum):
    """
    EducationLevel enumerated type with fuzzy matching.
    """

    pre_primary = "Pre-Primary"
    pre_básica = "Pre-Primary"
    primary = "Primary"
    básica = "Primary"
    middle = "Middle"
    media = "Middle"
    secondary = "Secondary"
    _9_ybe = "Pre-Primary"
    _12_ybe = "Pre-Primary"
    a_level = "Secondary"
    b_level = "Secondary"
    polytechnic = "Polytechnic"
    college = "University"
    university = "University"
    technical = "Polytechnic"
    vocational = "Polytechnic"
    vtc = "Polytechnic"
    tss = "Polytechnic"
    disability = "Polytechnic"
    nursing = "Polytechnic"
