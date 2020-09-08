"""
Enumerated type for cellular service type (seems redundant with the Connectivity type, but unicef db schema
defines them separately).
"""
from pydantic import BaseModel


class TowerTypeService(BaseModel):
    """Enum"""

    _2g = "2G"
    _3g = "3G"
    _4g = "4G"
    _5g = "5G"
    _6g = "6G"
    wifi = "WiFi"
