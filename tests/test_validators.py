"""Tests for validators module."""
from decimal import Decimal
import pytest

from src.calculator.validators import parse_decimal, validate_operation, validate_request_payload
from src.calculator.exceptions import ValidationError


def test_parse_decimal_from_string():
    assert parse_decimal("3.50") == Decimal("3.50")


def test_parse_decimal_from_int():
    assert parse_decimal(2) == Decimal("2")


def test_parse_decimal_from_float():
    # float converted via str() in the implementation
    assert parse_decimal(1.5) == Decimal(str(1.5))


def test_parse_decimal_invalid_string_raises():
    with pytest.raises(ValidationError):
        parse_decimal("abc")


def test_validate_operation_synonyms():
    assert validate_operation("+") == "add"
    assert validate_operation("Add") == "add"
    assert validate_operation("times") == "multiply"
