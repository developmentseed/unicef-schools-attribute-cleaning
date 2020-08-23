"""unicef_schools_attribute_cleaning module."""

from setuptools import find_packages, setup

with open("README.md") as f:
    readme = f.read()

# Runtime Requirements.
inst_reqs = [
    "click~=7.1.2",
    "pydantic~=1.6.1",
    "email-validator~=1.1.1",
    "pydantic[email]",
    "iso3166~=1.0.1",
]

# Dev Requirements
extra_reqs = {
    "test": ["pytest", "pytest-cov"],
    "dev": ["pytest", "pytest-cov", "pre-commit"],
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
