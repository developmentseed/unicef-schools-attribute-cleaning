"""Test unicef_schools_attribute_cleaning functions."""

from unicef_schools_attribute_cleaning import app


def test_app():
    """Test app.main function."""
    assert app.main("ah ", 3) == "ah ah ah "
