"""
Fuzzy Matching Enum
"""
import logging

from aenum import Enum
from fuzzywuzzy import process
from fuzzywuzzy.fuzz import token_set_ratio as scorer


class FuzzyMatchingEnum(Enum):
    """
    aenum Enum subclass implementing fuzzy matching in the _missing_name_ hook.
    """

    def __str__(self):
        """Override the str() other it will print ClassName.{attribute_name} instead of value."""
        return str(self.value)

    @classmethod
    def _missing_name_(cls, name: str):
        """
        Fuzzy matches the attribute names, returning closest one.

        :param name: attribute name
        :return: attribute from FuzzyMatchingEnum
        :raises: AttributeError
        """
        logger = logging.getLogger(f"{__name__}.{cls.__name__}")
        if name is None:
            raise AttributeError("attribute cannot be None")
        query = name
        choices = [name for name, member in cls.__members__.items()]
        result = process.extractOne(
            query, choices, score_cutoff=40, scorer=scorer
        )  # TODO don't hardcode score_cutoff
        if result is not None:
            (choice, score) = result
            # if score < 100:
            #     logger.info(f"matched {name} to {choice} ({score} score)")
            return cls[choice]
        logger.warning(f"{cls} has no fuzzy match for '{name}', choices = {choices}")
        raise AttributeError(f"unknown Connectivity: {name}")
