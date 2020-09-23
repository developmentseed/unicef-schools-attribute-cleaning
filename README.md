<p align="center">
  <a href="https://github.com/developmentseed/unicef-schools-attribute-cleaning/actions?query=workflow%3ACI" target="_blank">
      <img src="https://github.com/developmentseed/unicef-schools-attribute-cleaning/workflows/CI/badge.svg" alt="Test">
  </a>
</p>


# UNICEF Schools Attribute Cleaning

UNICEF schools attribute data cleaning for [UNICEF's Project Connect](https://www.projectconnect.world/).
Project Connect aims to map school connectivity globally and eliminate the digital divide.

## Summary

This repository hosts a Python package which performs data cleaning and enhancement as part of a Machine Learning
workflow developed in cooperation with UNICEF and [Development Seed](https://developmentseed.org/).

The scripts take as input tabular data in Delimited Text (`.csv`) or Excel (`.xlsx`) format, and perform a series of 
transformations and quality checks. The `dataframe_cleaner` is the main entry point for the Python user working with 
Pandas dataframes, e.g. in a Jupyter notebook. Here are the steps of the workflow:

- Apply user (data analyst) provided values to constant fields, including `country_code`, `is_private`
    `provider`, and `provider_is_private`. These handful of fields values are only known in advance by the user, so are 
    allowed as  parameters when running the cleaner script.
- Standardize the column names according to UNICEF's database ETL schema. The schema, originally provided as an Excel
    sheet, is encoded in the [unicef_schools_attribute_cleaning/models/](unicef_schools_attribute_cleaning/models/) module, 
    which uses [Pydantic](https://pydantic-docs.helpmanual.io/) classes. The column name standardization is a series of 
    steps:
    1. exact match on schema column name, e.g. `num_teachers -> num_teachers`
    2. exact match on schema column name aliases, e.g. `connectiontype -> type_connectivity`
    3. fuzzy match on schema column names and aliases, e.g. `School Name -> name`
    4. rename matched columns
    5. add missing columns
    6. remove invalid/unknown columns 
- Filter out any records missing location data in `lon`, `lat` columns. The location data is needed for subsequent
    enhancement steps, as well as for DevSeed's data validation work.
- Field-level validation: each row is passed through a Pydantic validation
    class which through a combination of coercion and validation, ensures conformance with the schema. Examples are 
    implemented for scenarios like:
    - Simple types like `string`, `float`, `integer`
    - Enumerated types such as `SchoolType` being one of Private, Government, or Religious.
        - Aliasing and Fuzzy matching is supported on Enumerated types, for example `básica -> Primary`.
    - Constraints like validating an `altitude` in meters to a valid range, and `lon`, `lat` being
    valid in decimal degrees.
- Reverse-geocode the `lon`, `lat` in  [Database of Global Administrative Areas (GADM)](https://gadm.org):
    1. When a match is found, fill in as many of the `admin0`, `admin1` ... `admin4` fields are available.
    Additionally, fill in the `admin_code` and `admin_id` fields with the GADM version and the unique ids of the
    matching GADM record.
    2. When a match is not found, buffer the location by 5Km and re-try the reverse geocode operation. At country 
    borders this will frequently resolve the unmatched records. We are assuming this is because the 
    GADM polygons have insufficient level-of-detail for border schools.
    3. If a match is still not found, then log a WARNING message including the school name.
- Runs Pandas `convert_dtypes()` to make it aware of the new column data types produced by the previous steps. 
- Then the notebook user can optionally save Pandas dataframe to `.csv` for other processing or visualization.

## Python and Jupyter Notebook usage

### Requirements

- Python 3.6 - 3.8 (3.8 recommended) with `pip`
- Git: This is written as a Python package, but it is only hosted on Github, so Git is required to get started. 

### Setup Python package

```shell script
git clone https://github.com/developmentseed/unicef-schools-attribute-cleaning.git
cd unicef-schools-attribute-cleaning/
pip install -e .
```

optional, to run in a jupyter notebook:

```shell script
pip install jupyterlab
jupyter lab
```

### Python Usage

```python
# an excerpt of a script - see Jupyter notebooks below for more context.

from iso3166 import countries
from unicef_schools_attribute_cleaning.pandas.dataframe_cleaner import dataframe_cleaner

country = countries.get('KE')
df = dataframe_cleaner(
    dataframe=src_df,
    country=country, # note that the country has to match the source data's country
    is_private=True,
    provider='MOE',
    provider_is_private=True
)
```

### Jupyter Notebooks

Each of the source data files for each country has it's own demo notebook:

| Country | Notebook |
| ------- | -------- |
| Honduras | [unicef_schools_attribute_cleaning/notebooks/honduras_demo.ipynb](unicef_schools_attribute_cleaning/notebooks/honduras_demo.ipynb) |
| Kazakhstan | [unicef_schools_attribute_cleaning/notebooks/kazakhstan_demo.ipynb](unicef_schools_attribute_cleaning/notebooks/kazakhstan_demo.ipynb) |
| Kenya Liquid | [unicef_schools_attribute_cleaning/notebooks/kenya_liquid_demo.ipynb](unicef_schools_attribute_cleaning/notebooks/kenya_liquid_demo.ipynb) |
| Kenya MOE | [unicef_schools_attribute_cleaning/notebooks/kenya_moe_demo.ipynb](unicef_schools_attribute_cleaning/notebooks/kenya_moe_demo.ipynb) |
| Kenya USAID | [unicef_schools_attribute_cleaning/notebooks/kenya_usaid_demo.ipynb](unicef_schools_attribute_cleaning/notebooks/kenya_usaid_demo.ipynb) |
| Rwanda | [unicef_schools_attribute_cleaning/notebooks/rwanda_demo.ipynb](unicef_schools_attribute_cleaning/notebooks/rwanda_demo.ipynb) |
| Sierra Leone | [unicef_schools_attribute_cleaning/notebooks/sierra_leone_demo.ipynb](unicef_schools_attribute_cleaning/notebooks/sierra_leone_demo.ipynb) |
| Zimbabwe | [unicef_schools_attribute_cleaning/notebooks/zimbabwe_demo.ipynb](unicef_schools_attribute_cleaning/notebooks/zimbabwe_demo.ipynb) |

## Adding support for a new data source

Each time running the `dataframe_cleaner` script on a new source data file, or a new country, 
some enhancements may need to be added to the `unicef_schools_attribute_cleaning/models` module.
This would be indicated by ERROR and WARNING level log information when running `dataframe_cleaner`,
or indicated when expected columns are missing from the resulting dataframe.

For example when running on the Kazakhstan data, some aliases had to be added to the 
`models/SchoolType.py`:

```
@@ -10,3 +10,6 @@ class SchoolType(FuzzyMatchingEnum):
    private = "Private"
    government = "Government"
    religious = "Religious"
+   Коммунальная_собственность = "Government"  # literally: Communal property
+   Собственность_предприятий = "Private"  # literally: Enterprise property
+   Собственность_иностранных_физических_лиц_Частная_собственность = "Private"
```

Enhancements might also need to be made to `models/School.py` and `models/School_aliases.py` 
depending on the source data. Sometimes, workarounds using Pandas may be required, to wrangle the data before sending 
it through `dataframe_cleaner`. Some of these examples are shown in the Jupyter Notebooks above.

## Contributing

This python package is based on [python-seed](https://github.com/developmentseed/python-seed).
It uses

- [tox](https://tox.readthedocs.io/en/latest/) for a test runner and for code coverage runner.
- `pytest` may also be run from the repository's root.
- `pre-commit` is also used to run isort, flake8, pydocstyle, black, example usage is
  `pre-commit install` and `pre-commit run --all-files`.
