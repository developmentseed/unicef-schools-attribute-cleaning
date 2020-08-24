#!/usr/bin/env python

"""
Dump the Pydantic model's fields into a json file.
This is a hack/workaround for the fuzzy_alias_generator.py module having a circular import with the School.py.
"""

import inspect
import os

from unicef_schools_attribute_cleaning.models.School import School


def _main():
    models_dir = os.path.dirname(inspect.getfile(School))
    schema = School.schema_json()
    target = f"{models_dir}/School_schema.json"
    with open(target, "w") as fp:
        fp.write(schema)


if __name__ == "__main__":
    _main()
