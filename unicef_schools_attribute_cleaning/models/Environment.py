"""
Enumerated type for regional school environment
"""
from .FuzzyMatchingEnum import FuzzyMatchingEnum


class Environment(FuzzyMatchingEnum):
    """
    Environment enumerated type with fuzzy matching.
    """

    urban = "Urban"
    rural = "Rural"
    semi_rural = "Semi-Rural"
