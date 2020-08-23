#!/usr/bin/env python

"""
Dump the Pydantic model's fields into a json file.
This is a hack/workaround for the fuzzy_alias_generator.py module having a circular import with the School.py.
"""
from unicef_schools_attribute_cleaning.models.School import School

schema = School.schema_json()
with open("School_schema.json", "w") as fp:
    fp.write(schema)
