"""
Enumerated type for internet connectivity.
"""
from pydantic import BaseModel

# TODO how to instantiate enumerated type in School -> Connectivity?
# E   pydantic.error_wrappers.ValidationError: 1 validation error for School
# E   type_connectivity
# E     value is not a valid dict (type=type_error.dict)


class Connectivity(BaseModel):
    """Enum"""

    class Config:
        """TODO"""

        arbitrary_types_allowed = True

    _2g = "2G"
    _3g = "3G"
    _4g = "4G"
    _5g = "5G"
    _6g = "6G"
    fiber = "Fiber"
    cable = "Cable"
    dsl = "DSL"
    satellite = "Satellite"
