"""
Enumerated type for internet connectivity.
"""
from pydantic import BaseModel


class Connectivity(BaseModel):
    """Enum"""

    _2g = "2G"
    _3g = "3G"
    _4g = "4G"
    _5g = "5G"
    _6g = "6G"
    fiber = "Fiber"
    cable = "Cable"
    dsl = "DSL"
    satellite = "Satellite"
