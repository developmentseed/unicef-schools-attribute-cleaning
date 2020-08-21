"""
Enumerated type for school regional environment.
"""

from pydantic import BaseModel


class Environment(BaseModel):
    """Enum"""

    urban = "Urban"
    semi_rural = "Semi-Rural"
