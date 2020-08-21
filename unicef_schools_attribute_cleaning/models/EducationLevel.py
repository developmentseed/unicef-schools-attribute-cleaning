"""
Enumerated type for education level.
"""
from pydantic import BaseModel


class EducationLevel(BaseModel):
    """Enum"""

    primary = "Primary"
    secondary = "Secondary"
