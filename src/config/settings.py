"""
Configuration settings for WebCalc2.
Loads environment variables from a .env file (if present) and exposes
configuration constants used across the application.

Type hints are provided where applicable.
"""
from __future__ import annotations

import os
from typing import Final
from dotenv import load_dotenv

# Load environment variables from .env in project root if available
load_dotenv()

# Decimal and application configuration
DECIMAL_PRECISION: Final[int] = int(os.getenv("DECIMAL_PRECISION", "28"))
DECIMAL_ROUNDING: Final[str] = os.getenv("DECIMAL_ROUNDING", "ROUND_HALF_EVEN")

# Flask configuration
DEBUG: Final[bool] = os.getenv("DEBUG", "False").lower() in ("1", "true", "yes")
SECRET_KEY: Final[str] = os.getenv("SECRET_KEY", "change-this-in-production")

# Logging
LOG_LEVEL: Final[str] = os.getenv("LOG_LEVEL", "INFO")

# Expose here for easy import from other modules
__all__ = [
    "DECIMAL_PRECISION",
    "DECIMAL_ROUNDING",
    "DEBUG",
    "SECRET_KEY",
    "LOG_LEVEL",
]
