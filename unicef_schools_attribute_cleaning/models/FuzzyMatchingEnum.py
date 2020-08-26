"""
Fuzzy Matching Enum
"""
import logging

from aenum import Enum
from fuzzywuzzy import process


class FuzzyMatchingEnum(Enum):
    """
    aenum Enum subclass implementing fuzzy matching in the _missing_name_ hook.
    """

    def __str__(self):
        """Override the str() other it will print ClassName.attr instead of value."""
        return str(self.value)

    @classmethod
    def _missing_name_(cls, name):
        if name is None:
            raise AttributeError("attribute cannot be None")
        query = name
        choices = [name for name, member in cls.__members__.items()]
        result = process.extractOne(
            query, choices, score_cutoff=80
        )  # TODO don't hardcode score_cutoff
        if result is not None:
            (choice, score) = result
            # logging.info(f"matched {name} to {choice} ({score} score)")
            return cls[choice]
        logging.warning(f"no fuzzy match for '{name}', choices = {choices}")
        raise AttributeError(f"unknown Connectivity: {name}")
