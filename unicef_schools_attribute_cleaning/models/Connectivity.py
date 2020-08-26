"""
Internet Connectivity enumerated type with fuzzy matching.
"""
import logging

from aenum import Enum
from fuzzywuzzy import process


class Connectivity(Enum):
    """
    Internet Connectivity enumerated type with fuzzy matching.
    """

    _2g = "2G"
    _3g = "3G"
    _4g = "4G"
    lte = "4G"
    _4G = "4G"
    _5g = "5G"
    _6g = "6G"
    dsl = "DSL"
    adsl = "DSL"
    fiber = "Fiber"
    fiber_optic = "Fiber"
    p2p = "P2P Wireless"
    radio_link = "P2P Wireless"
    satellite = "Satellite"
    vsat = "Satellite"
    dial_up = "Dial Up"
    dialup = "Dial Up"
    dongle = "Dongle"
    broadband = "Broadband"

    @classmethod
    def _missing_name_(cls, name):
        if name is None:
            raise AttributeError("attribute cannot be None")
        query = name
        choices = [name for name, member in cls.__members__.items()]
        result = process.extractOne(query, choices, score_cutoff=80)
        if result is not None:
            (choice, score) = result
            # logging.warning(f'matched {name} to {choice} ({score} score)')
            return cls[choice]
        logging.warning(f"no fuzzy match for {name}, choices = {choices}")
        raise AttributeError(f"unknown Connectivity: {name}")


# Connectivity = Enum('Connectivity', [
#     ('4g', '4G'),
#     ('4G', '4G'),
#     ('LTE', 'LTE')
# ], type=BaseConnectivity)


#
# class Connectivity(str, Enum):
#     """Internet Connectivity"""
#     'x2g' = '2g'
#     '3g' = auto()
#     '4g' = auto()
#     lte = '4g'
#     '5g' = auto()
#     '6g' = auto()
#     fiber = auto()
#     cable = auto()
#     dsl = "DSL"
#     adsl = "DSL"
#     shdsl = "DSL"
#     xdsl = "DSL"
#     satellite = "Satellite"
#     radio = "Radio"
#
