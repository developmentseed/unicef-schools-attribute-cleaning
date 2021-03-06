"""
School aliases: these were logged as "manual_fix" fields in devseed map data team's validation work.
The canonical field name and it's aliases will be used as inputs to the fuzzy matcher, if no exact matches are found.
"""

School_aliases = dict(
    country_code=[],
    admin0=["country"],
    admin1=["state", "dept"],
    admin2=["county", "province"],
    admin3=["district"],
    admin4=["location"],
    admin_code=[],
    admin_id=[],
    name=["idschool_name", "school"],
    address=[],
    address2=[],
    phone_number=["phone"],
    person_contact=["contact", "respondent_name"],
    email=[],
    postal_code=["zip code", "zip"],
    lon=["longitude", "lng", "long", "geopointlongitude"],
    lat=["latitude", "geopointlatitude"],
    altitude=["geopointaltitude"],
    gps_confidence=[],
    date=[],
    num_students=["enrollment"],
    num_teachers=[],
    connectivity=[],
    type_connectivity=["connectiontype"],
    speed_connectivity=[],
    latency_connectivity=[],
    availability_connectivity=[],
    num_computers=["computers_number", "tot_func_computers"],
    type_school=["status of school"],
    educ_level=["school level", "settings in school", "sch_type", "level of education"],
    environment=[],
    num_classrooms=[],
    num_sections=[],
    water=[],
    electricity=[],
    num_latrines=[],
    provider=[],
    description=["school number"],
    last_update=[],
    tower_dist=[],
    tower_type_service=[],
    tower_type=[],
    tower_code=[],
    tower_latitude=[],
    tower_longitude=[],
    owner=[],
    is_private=[],
    provider_is_private=[],
    uuid=[],
)
