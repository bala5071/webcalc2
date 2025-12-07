"""Core calculator logic using Decimal for precise arithmetic.

Provides Calculator class with static arithmetic methods and a compute helper.
All methods use decimal context configured from src.config.settings.
"""
from __future__ import annotations

from decimal import Decimal, getcontext
from typing import Callable, Dict

from ..config import settings
from .exceptions import DivisionByZeroError, ValidationError

# Configure global decimal context according to settings
_ctx = getcontext()
_ctx.prec = int(settings.DECIMAL_PRECISION)
# Use getattr on decimal module to fetch rounding constant; fallback to ROUND_HALF_EVEN
import decimal as _decimal_module
_ctx.rounding = getattr(_decimal_module, settings.DECIMAL_ROUNDING, _decimal_module.ROUND_HALF_EVEN)


class Calculator:
    """Calculator exposes basic arithmetic operations using Decimal.

    Methods are static and pure (no side effects). The compute() helper maps
    operation tokens to the corresponding arithmetic method.
    """

    @staticmethod
    def add(a: Decimal, b: Decimal) -> Decimal:
        """Return a + b using Decimal arithmetic.

        Args:
            a: Decimal operand
            b: Decimal operand

        Returns:
            Decimal: sum of a and b
        """
        return a + b

    @staticmethod
    def subtract(a: Decimal, b: Decimal) -> Decimal:
        """Return a - b using Decimal arithmetic."""
        return a - b

    @staticmethod
    def multiply(a: Decimal, b: Decimal) -> Decimal:
        """Return a * b using Decimal arithmetic."""
        return a * b

    @staticmethod
    def divide(a: Decimal, b: Decimal) -> Decimal:
        """Return a / b using Decimal arithmetic.

        Raises:
            DivisionByZeroError: if b is zero.
        """
        if b == Decimal("0"):
            raise DivisionByZeroError("Cannot divide by zero")
        # Using Decimal context for precision/rounding
        return a / b

    @staticmethod
    def _normalize_operation(operation: str) -> str:
        """Normalize operation token to canonical form.

        Accepts canonical names 'add','subtract','multiply','divide' and symbols
        as provided by validators (so in general this should already be canonical).
        """
        if not operation:
            raise ValidationError("Unsupported operation: ''")
        return str(operation).strip().lower()

    @staticmethod
    def compute(a: Decimal, b: Decimal, operation: str) -> Decimal:
        """Compute result for given operands and operation token.

        Supported operations: 'add', 'subtract', 'multiply', 'divide', and corresponding symbols.

        Args:
            a: Decimal operand
            b: Decimal operand
            operation: operation token

        Returns:
            Decimal: computation result

        Raises:
            ValidationError: if operation unsupported
            DivisionByZeroError: if dividing by zero
        """
        op = Calculator._normalize_operation(operation)
        mapping: Dict[str, Callable[[Decimal, Decimal], Decimal]] = {
            "add": Calculator.add,
            "subtract": Calculator.subtract,
            "multiply": Calculator.multiply,
            "divide": Calculator.divide,
        }
        func = mapping.get(op)
        if func is None:
            raise ValidationError(f"Unsupported operation: '{operation}'")
        return func(a, b)


__all__ = ["Calculator"]
