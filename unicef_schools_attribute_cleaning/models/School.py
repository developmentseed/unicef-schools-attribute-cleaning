"""
Pydantic model for Schools, sourced from the schema in Project_Connect_School_Schema_UNICEF_DB.xlsx
"""
from datetime import datetime
from math import isclose
from typing import Optional
from uuid import UUID

from iso3166 import countries
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    PositiveFloat,
    PositiveInt,
    confloat,
    conint,
    constr,
    root_validator,
    validator,
)

from ..utils.none_words import none_words
from .Connectivity import Connectivity
from .EducationLevel import EducationLevel
from .Environment import Environment
from .Latitude import Latitude
from .Longitude import Longitude
from .Percentage import Percentage
from .SchoolType import SchoolType
from .TowerTypeService import TowerTypeService


class School(BaseModel):
    """Pydantic model"""

    country_code: constr(min_length=2, max_length=2) = Field(
        ...
    )  # ISO Alpha-2 Code (US, ES,…) (Required)
    admin0: Optional[str]  # Country
    admin1: Optional[str]  # State / Dept
    admin2: Optional[str]  # County / Province
    admin3: Optional[str]  # District /
    admin4: Optional[str]  # Location
    admin_code: Optional[str]  # local code(xx - yy - zz)
    admin_id: Optional[
        str
    ]  # string that identifies uniquely the geographic admin , and easy to spotcheck: CountryCode_GADM Version _ Index (admin0) _ Index (admin1) _Index (admin2) _ downcase of admin
    name: str = Field(...)  # string: Amazonas (Required)
    address: Optional[str]
    address2: Optional[str]  # Number on street
    phone_number: Optional[str]
    person_contact: Optional[str]  # string: name
    email: Optional[EmailStr]
    postal_code: Optional[str]
    lon: Longitude = Field(...)  # longitude (Required)
    lat: Latitude = Field(...)  # latitude (Required)
    altitude: Optional[
        confloat(ge=-411, le=8850)
    ]  # number[m]  min and max are for the world (meters)
    gps_confidence: Optional[Percentage]  # number[%]
    date: Optional[datetime]  # date when it was created
    num_students: Optional[int]  # of students
    num_teachers: Optional[int]  # of teachers
    connectivity: Optional[bool]  # internet connectivity
    type_connectivity: Optional[Connectivity]
    speed_connectivity: Optional[
        confloat(ge=0, le=12500000)
    ]  # number[kbps] 12500000 kbps is ~100 gigabit/sec
    latency_connectivity: Optional[
        confloat(ge=0, le=5000)
    ]  # number[ms]  5000 ms is ~5 seconds
    availability_connectivity: Optional[Percentage]  # number [%]
    num_computers: Optional[conint(ge=0)]  # of computers/tablets
    type_school: Optional[
        SchoolType
    ]  # type of school(private, government, religious???
    educ_level: Optional[EducationLevel]  # primary, secondary,…
    environment: Optional[Environment]  # Urban, semi - rural, rural
    num_classrooms: Optional[PositiveInt]  # of classrooms
    num_sections: Optional[PositiveInt]  # of sections
    water: Optional[bool]  # Yes / No
    electricity: Optional[bool]  # Yes / No
    num_latrines: Optional[PositiveInt]  # of latrines
    provider: Optional[str]
    description: Optional[str]
    last_update: Optional[datetime]
    tower_dist: Optional[PositiveFloat]  # number[km]
    tower_type_service: Optional[TowerTypeService]  # (2G, 3G, 4G, Wifi)
    tower_type: Optional[str]
    tower_code: Optional[str]
    tower_latitude: Optional[Latitude]
    tower_longitude: Optional[Longitude]
    owner: str = Field(...)  # ProCo(vs UNICEF, ...) (Required)
    is_private: bool = Field(...)  # (Required)
    provider_is_private: bool = Field(...)  # (Required)
    # TODO: make uuid required in output schema?
    uuid: Optional[
        UUID
    ]  # unique id generated by devseed ML training data validation scripts

    @validator("type_connectivity", pre=True)
    def check_type_connectivity(cls, raw_val):
        """
        Before field validation occurs, filter down to strings and than index into the Connectivity enum.
        """
        if not isinstance(raw_val, str):
            return None
        if raw_val.lower() in none_words:
            return None
        try:
            return Connectivity[raw_val]
        except (KeyError, AttributeError):
            return None
        return None

    @validator("educ_level", pre=True)
    def check_educ_level(cls, raw_val):
        """
        Before field validation occurs, filter down to strings and than index into the EducationLevel enum.
        """
        if not isinstance(raw_val, str):
            return None
        if raw_val.lower() in none_words:
            return None
        try:
            return EducationLevel[raw_val]
        except (KeyError, AttributeError):
            return None
        return None

    @validator("country_code", pre=True)
    def check_country_code(cls, val):
        """
        Pre-process and validate country codes. ISO 3166-1 defines two-letter, three-letter, and three-digit country
        codes.
        """
        try:
            c = countries.get(val)
            return c.alpha2
        except KeyError:
            pass
        raise ValueError(f"invalid country, expected ISO 3166 code, got {val}")

    # @validator('lat', pre=True)
    # def check_lat(cls, val):
    #     if isinstance(val, str) and val.lower() in none_words:
    #         logging.warning(f'{val} -> None')
    #         return None
    #     logging.warning(f'check_lat: {val} (type={type(val)})')
    #     return val

    @root_validator
    def check_lat_lng_for_null_island(cls, values):
        """
        Null island check for lat, lng fields.
        """
        lat = values.get("lat")
        lon = values.get("lon")
        if lat is not None and lon is not None:
            if isclose(lat, 0.0) and isclose(lon, 0.0):
                name = values.get("name")
                uuid = values.get("uuid")
                raise ValueError(
                    f"invalid lat,lon of 0,0 for name: {name}, uuid: {uuid}"
                )
        return values

    @root_validator
    def check_tower_lat_lng_for_null_island(cls, values):
        """
        Null island check for tower_latitude, tower_longitude fields.
        """
        lat = values.get("tower_latitude")
        lon = values.get("tower_longitude")
        if lat is not None and lon is not None:
            if isclose(lat, 0.0) and isclose(lon, 0.0):
                name = values.get("name")
                uuid = values.get("uuid")
                raise ValueError(
                    f"invalid tower_latitude,tower_longitude of 0,0 for name: {name}, uuid: {uuid}"
                )
        return values
