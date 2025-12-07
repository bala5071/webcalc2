"""Custom exceptions for WebCalc2 calculator module."""
from __future__ import annotations

from typing import Final


class CalculatorError(Exception):
    """Base exception type for calculator errors.

    All custom calculator exceptions derive from this class so callers can
    catch a single base type when desired.
    """


class ValidationError(CalculatorError):
    """Raised when input validation fails (bad payload, unsupported operation, etc.)."""


class DivisionByZeroError(CalculatorError):
    """Raised when attempting to divide by zero."""


class CalculationError(CalculatorError):
    """Raised for generic calculation failures not covered by other types."""
