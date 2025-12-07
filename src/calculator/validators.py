"""Validation utilities for WebCalc2 calculator API.

Functions:
- parse_decimal(value) -> Decimal: safely converts a value to Decimal and validates finiteness
- validate_operation(operation) -> str: canonicalize and validate operation token
- validate_request_payload(payload) -> tuple[Decimal, Decimal, str]: validate JSON payload

All public functions raise ValidationError on invalid input.
"""
from __future__ import annotations

from decimal import Decimal, InvalidOperation
from typing import Tuple, Any

from .exceptions import ValidationError

_OPERATION_MAP = {
    "add": "add",
    "+": "add",
    "plus": "add",
    "subtract": "subtract",
    "-": "subtract",
    "minus": "subtract",
    "multiply": "multiply",
    "*": "multiply",
    "x": "multiply",
    "times": "multiply",
    "divide": "divide",
    "/": "divide",
}


def _to_str_safe(value: Any) -> str:
    """Convert a supported value to string safely, stripping whitespace.

    This function ensures numbers like floats are converted via str(value)
    (caller is responsible for avoiding direct float-to-Decimal pitfalls).
    """
    if value is None:
        raise ValidationError("Numeric value is required")
    s = str(value).strip()
    if s == "":
        raise ValidationError("Numeric value is required")
    return s


def parse_decimal(value: Any) -> Decimal:
    """Parse value into Decimal.

    Accepts str, int, float (or Decimal). Floats are converted via str()
    to avoid introducing binary floating point artifacts where possible.

    Raises:
        ValidationError: if value cannot be parsed or is not finite.
    """
    try:
        if isinstance(value, Decimal):
            d = value
        else:
            s = _to_str_safe(value)
            d = Decimal(s)
    except (InvalidOperation, ValueError) as exc:  # ValueError for weird inputs
        raise ValidationError(f"Invalid numeric value: '{value}'") from exc

    # Ensure value is finite (no NaN, Infinity)
    if not d.is_finite():
        raise ValidationError(f"Numeric value must be finite: '{value}'")

    return d


def validate_operation(operation: Any) -> str:
    """Validate and canonicalize operation token.

    Returns one of: 'add', 'subtract', 'multiply', 'divide'.
    Raises ValidationError if unsupported.
    """
    if operation is None:
        raise ValidationError("Operation is required")
    key = str(operation).strip().lower()
    if key in _OPERATION_MAP:
        return _OPERATION_MAP[key]
    raise ValidationError(
        f"Unsupported operation: '{operation}'. Supported operations: add, subtract, multiply, divide"
    )


def validate_request_payload(payload: Any) -> Tuple[Decimal, Decimal, str]:
    """Validate incoming JSON payload and return parsed operands and operation.

    Expected payload shape: dict with keys 'operand1', 'operand2', 'operation'.

    Returns:
        (operand1_decimal, operand2_decimal, canonical_operation)

    Raises:
        ValidationError: on missing keys or invalid values.
    """
    if not isinstance(payload, dict):
        raise ValidationError("JSON object expected")

    if "operand1" not in payload:
        raise ValidationError("operand1 is required and must be a numeric value")
    if "operand2" not in payload:
        raise ValidationError("operand2 is required and must be a numeric value")
    if "operation" not in payload:
        raise ValidationError("operation is required and must be a supported token")

    a = parse_decimal(payload["operand1"])
    b = parse_decimal(payload["operand2"])
    op = validate_operation(payload["operation"])
    return a, b, op
