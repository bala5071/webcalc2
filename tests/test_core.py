"""Unit tests for calculator core logic."""
from decimal import Decimal
import pytest

from src.calculator.core import Calculator
from src.calculator.exceptions import DivisionByZeroError


def test_add_two_decimals():
    assert Calculator.add(Decimal("1.1"), Decimal("2.2")) == Decimal("3.3")


def test_subtract_negative_result():
    assert Calculator.subtract(Decimal("1"), Decimal("2")) == Decimal("-1")


def test_multiply_by_decimal():
    assert Calculator.multiply(Decimal("1.5"), Decimal("2")) == Decimal("3.0")


def test_divide_valid():
    assert Calculator.divide(Decimal("1"), Decimal("4")) == Decimal("0.25")


def test_divide_by_zero_raises():
    with pytest.raises(DivisionByZeroError):
        Calculator.divide(Decimal("1"), Decimal("0"))
