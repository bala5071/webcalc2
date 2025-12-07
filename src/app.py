"""Flask application factory for WebCalc2.

Provides create_app factory that configures logging, routes and error handling.

Endpoints:
- GET / -> renders index.html
- POST /api/calculate -> accepts JSON body with operand1, operand2, operation

All JSON error responses follow the shape:
{"status":"error","error":{"code":...,"message":...}}

"""
from __future__ import annotations

import logging
import os
from datetime import datetime, timezone
from typing import Any, Dict, Tuple

from flask import Flask, request, jsonify, render_template, Response

from .calculator.validators import validate_request_payload
from .calculator.core import Calculator
from .calculator.exceptions import (
    CalculatorError,
    ValidationError,
    DivisionByZeroError,
)
from .config import settings


def _json_response(payload: Dict[str, Any], status: int = 200) -> Tuple[Response, int]:
    """Return a Flask JSON response with given payload and HTTP status.

    Args:
        payload: JSON-serializable dictionary
        status: HTTP status code
    """
    return jsonify(payload), status


def create_app(config_overrides: dict | None = None) -> Flask:
    """Create and configure the Flask application.

    Args:
        config_overrides: Optional dict of Flask config overrides useful for testing.

    Returns:
        Flask app instance
    """
    app = Flask(__name__, static_folder="static", template_folder="templates")

    # Basic config
    app.config["DEBUG"] = settings.DEBUG
    app.config["SECRET_KEY"] = settings.SECRET_KEY

    # Apply overrides if provided (useful in tests)
    if config_overrides:
        app.config.update(config_overrides)

    # Logging configuration
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)
    app.logger.setLevel(log_level)
    app.logger.addHandler(console_handler)

    # File handler (write to project root webcalc2.log)
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    log_path = os.path.join(project_root, "webcalc2.log")
    try:
        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(log_level)
        app.logger.addHandler(file_handler)
    except Exception:
        app.logger.warning("Unable to create file handler for logging at %s", log_path)

    @app.route("/", methods=["GET"])
    def index():
        """Render the single-page calculator UI."""
        return render_template("index.html")

    @app.route("/api/calculate", methods=["POST"])
    def api_calculate():
        """API endpoint to perform arithmetic operations.

        Expects JSON body with keys: operand1, operand2, operation
        Returns a JSON response with status and data/error fields.
        """
        try:
            payload = request.get_json(force=True)
        except Exception as exc:  # pragma: no cover - defensive
            app.logger.warning("Invalid JSON body: %s", exc)
            return _json_response(
                {"status": "error", "error": {"code": "invalid_json", "message": "Invalid JSON body"}},
                400,
            )

        try:
            a, b, operation = validate_request_payload(payload)
            app.logger.debug("Parsed request: operand1=%s operand2=%s operation=%s", a, b, operation)

            result = Calculator.compute(a, b, operation)

            # Format result as fixed-point string to avoid scientific notation in JSON
            result_str = format(result, "f")

            data = {
                "operand1": str(a),
                "operand2": str(b),
                "operation": operation,
                "result": result_str,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            app.logger.info("Calculation success: %s %s %s = %s", a, operation, b, result_str)
            return _json_response({"status": "success", "data": data}, 200)

        except DivisionByZeroError as ex:
            app.logger.warning("Division by zero: %s", ex)
            return _json_response(
                {"status": "error", "error": {"code": "division_by_zero", "message": str(ex)}} , 400
            )
        except ValidationError as ex:
            app.logger.warning("Validation error: %s", ex)
            return _json_response(
                {"status": "error", "error": {"code": "validation_error", "message": str(ex)}}, 400
            )
        except CalculatorError as ex:
            app.logger.error("Calculator error: %s", ex)
            return _json_response(
                {"status": "error", "error": {"code": "calculation_error", "message": str(ex)}}, 400
            )
        except Exception as ex:  # pragma: no cover - defensive
            app.logger.exception("Unhandled exception in api_calculate")
            return _json_response(
                {"status": "error", "error": {"code": "server_error", "message": "An internal error occurred"}} , 500
            )

    return app


if __name__ == "__main__":  # pragma: no cover - convenience run
    app = create_app()
    app.run(debug=app.config.get("DEBUG", False))
