import pytest
from lib.date_converter import DateConverter
def test_today():
    converter = DateConverter()
    actual = converter.fromString('today')
    expected = arrow.utcnow().format('DD.MM.YYYY')
    assert actual == expected