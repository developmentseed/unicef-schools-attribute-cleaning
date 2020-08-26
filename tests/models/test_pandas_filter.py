from pandas import Series

from unicef_schools_attribute_cleaning.models.school_pandas_filter import (
    school_pandas_filter,
)

from .test_School import src_fields


def test_filter():
    row = Series(src_fields)
    result = school_pandas_filter(row)
    assert result is not None, repr(result)
