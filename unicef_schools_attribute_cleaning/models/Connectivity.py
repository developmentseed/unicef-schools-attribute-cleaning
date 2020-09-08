"""
Internet Connectivity Enum
"""
from .FuzzyMatchingEnum import FuzzyMatchingEnum


class Connectivity(FuzzyMatchingEnum):
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
