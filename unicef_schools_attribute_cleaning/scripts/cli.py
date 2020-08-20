"""unicef_schools_attribute_cleaning.scripts.cli: unicef_schools_attribute_cleaning CLI."""

import click

from .. import version


@click.group(short_help="unicef_schools_attribute_cleaning CLI")
@click.version_option(version=version, message="%(version)s")
def unicef_schools_attribute_cleaning():
    """unicef_schools_attribute_cleaning subcommands."""
    pass


# @unicef_schools_attribute_cleaning.command(short_help="Validate COGEO")
# @click.option(...)
# def cmd(...):
#     """Do Great Things."""
#     pass
