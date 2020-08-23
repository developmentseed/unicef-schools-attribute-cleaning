"""
TODO
"""
import json
import logging
from os.path import dirname

from fuzzywuzzy import process

THRESHOLD = 90

# see ./dump_School_schema.py for notes about this hack :/
my_dir = dirname(__file__)
schema_fake = f"{my_dir}/School_schema.json"

with open(schema_fake) as json_file:
    schema = json.load(json_file)
    schema_fields = schema["properties"].keys()  # school_fields is a dict view

known_aliases = f"{my_dir}/School_aliases.json"


def generate_aliases(src_column_names: list) -> dict:
    """
    TODO
    """
    result = dict()
    for src_column_name in src_column_names:
        (match, score) = process.extractOne(src_column_name, schema_fields,)
        if score >= THRESHOLD:
            logging.warning(f"matched {src_column_name} -> {match} with score {score}")
        result[src_column_name] = match
    return result
