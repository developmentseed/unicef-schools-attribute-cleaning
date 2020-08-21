"""
Longitude: a float constrained to [-180, 180] degrees.
"""
from typing import Type

from pydantic import confloat

Longitude: Type[float] = confloat(ge=-180, le=180)
