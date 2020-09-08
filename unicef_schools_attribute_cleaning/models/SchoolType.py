"""
Enumerated type for categories of schools.
"""
from pydantic import BaseModel


class SchoolType(BaseModel):
    """Enum"""

    private = "Private"
    government = "Government"
    religious = "Religious"
