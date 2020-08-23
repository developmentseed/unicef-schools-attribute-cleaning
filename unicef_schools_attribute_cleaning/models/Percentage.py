"""
Percentage: a float constrained to [0, 100].
"""
from typing import Type

from pydantic import confloat

Percentage: Type[float] = confloat(ge=0, le=100)
