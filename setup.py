"""unicef_schools_attribute_cleaning module."""

from setuptools import find_packages, setup

with open("README.md") as f:
    readme = f.read()

# Runtime Requirements.
inst_reqs = [
    "aenum~=2.2.4",
    "click~=7.1.2",
    "email-validator~=1.1.1",
    "defusedxml~=0.6.0",
    "dependency-injector~=3.33.0",
    "diskcache~=5.0.2",
    "iso3166~=1.0.1",
    "openpyxl~=3.0.5",
    "pandas~=1.1.1",
    "pydantic[email]",
    "pydantic~=1.6.1",
    "python-Levenshtein~=0.12.0",
    "responses~=0.11.0",
    "requests~=2.24.0",
    "fuzzywuzzy==0.18.0",
    "xlrd~=1.2.0",
]

# Dev Requirements
extra_reqs = {
    "test": ["pytest", "pytest-cov"],
    "dev": ["pytest==6.0.1", "pytest-cov== 2.10.1", "pre-commit==2.7.1"],
}


setup(
    name="unicef_schools_attribute_cleaning",
    version="0.0.1",
    description=u"An Awesome python module",
    long_description=readme,
    long_description_content_type="text/markdown",
    python_requires=">=3",
    classifiers=[
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="An Awesome python module",
    author=u"",
    author_email="",
    url="",
    packages=find_packages(exclude=["ez_setup", "examples", "tests"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=inst_reqs,
    extras_require=extra_reqs,
    entry_points={
        "console_scripts": [
            "unicef_schools_attribute_cleaning = unicef_schools_attribute_cleaning.scripts.cli:unicef_schools_attribute_cleaning"
        ]
    },
)
