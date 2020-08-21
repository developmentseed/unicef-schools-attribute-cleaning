"""
Latitude: a float constrained to [-90, 90] degrees.
"""
from typing import Type

from pydantic import confloat

Latitude: Type[float] = confloat(ge=-90, le=90)
