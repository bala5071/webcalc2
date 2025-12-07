## 1. PROJECT OVERVIEW & OBJECTIVES

- Project root (fixed): C:\Users\balas\Documents\Projects\webcalc2

Problem Statement:
- Provide a simple, reliable web-based mathematical calculator that performs the four basic arithmetic operations — addition, subtraction, multiplication, and division — on two user-supplied numeric values (integers or decimals). The application must validate inputs, handle errors (including division by zero), produce consistent numeric results (use Decimal for precision), and provide both a simple web UI and a JSON API endpoint for programmatic use.

Target Users:
- End users who need a quick arithmetic calculator in a browser.
- Developers or automated systems that need a small HTTP API to do arithmetic.
- Students and testers who want a minimal web demo of arithmetic operations.

Core Functionality (3–5 main features):
1. Web UI (single page) where users can input two numbers and choose an operation (add, subtract, multiply, divide) and see results immediately.
2. JSON API endpoint (/api/calculate) that accepts two numeric operands and an operation and returns the result (and error messages when applicable).
3. Robust input validation and error handling (invalid numeric input, unsupported operation, division by zero).
4. Accurate decimal arithmetic using Python Decimal with configurable precision and rounding.
5. Unit tests and integration tests covering core logic and the API.

Success Criteria:
- UI accepts valid numeric inputs and returns correct results for all four operations.
- API returns JSON with HTTP 200 for valid requests and appropriate error codes (400) with clear messages for invalid requests.
- Division by zero returns a 400 with a descriptive message; server must not crash.
- Automated unit tests pass (target > 90% coverage for core modules).
- Project can be set up and run on Windows using the specified steps in this document.

Scope
- IN SCOPE:
  - Web UI (static HTML/CSS/JS) + Flask backend endpoints.
  - Input validation, numeric parsing, Decimal arithmetic, error handling.
  - Unit tests with pytest, integration tests for API endpoints.
  - Configuration via .env and settings module.
  - Logging to a local file and console.
  - Documentation and examples.
- OUT OF SCOPE:
  - User accounts, authentication, persistent storage/database.
  - Advanced math functions (sin, cos, log, etc).
  - Distributed deployment, containerization (Docker) or cloud infra.
  - Internationalization/localization beyond basic English.
  - Large-scale performance optimization.

## 2. TECHNOLOGY STACK (Specific Versions Required)

- Programming Language: Python 3.11.6
  - Why: Modern stable Python with wide ecosystem support and Decimal precision support. Works well on Windows.

- Core Web Framework: Flask==2.3.2
  - Why: Lightweight, easy to set up for simple web apps and APIs. Minimal overhead for this project.

- Key Libraries:
  - python-dotenv==1.0.0 # For loading .env environment variables into settings
  - pytest==7.4.0 # For unit and integration testing
  - pytest-flask==1.4.0 # For Flask test client integration tests
  - werkzeug==3.0.0 # (flask dependency) kept by pip resolution; included in requirements
  - Jinja2==3.1.2 # (flask dependency) templating for UI
  - decimal is part of Python standard library; no external package
  - bootstrap (static CSS) via CDN (no pip package required)
  - flake8==6.1.0 # Linter for development (optional but recommended)
  - black==24.1.0 # Formatter (optional but recommended)

- Database/Storage:
  - None required. All computation is ephemeral; no persistence.

- External Services/APIs:
  - None required.

- Development Tools:
  - Testing: pytest + pytest-flask
  - Linter: flake8==6.1.0
  - Formatter: black==24.1.0
  - Virtual environment: venv (Python standard)

Justification summary:
- Flask + Python provide the simplest path to deliver a web UI + JSON API with minimal code. Decimal ensures precision and deterministic behavior for decimals. pytest and pytest-flask give reliable test frameworks.

## 3. COMPLETE FILE & DIRECTORY STRUCTURE

Project root (must exist exactly at):
C:\Users\balas\Documents\Projects\webcalc2

Exact tree (files with descriptions and whether auto-generated):

```
C:\Users\balas\Documents\Projects\webcalc2\
├── src\
│   ├── __init__.py                  # Package marker (manually created)
│   ├── app.py                       # Flask application entry point (manually created)
│   ├── calculator\
│   │   ├── __init__.py              # package for calculator core (manually created)
│   │   ├── core.py                  # Calculator core logic and public API (manually created)
│   │   ├── exceptions.py            # Custom exceptions (manually created)
│   │   └── validators.py            # Input validation utilities (manually created)
│   ├── config\
│   │   ├── __init__.py              # package for config (manually created)
│   │   └── settings.py              # Loads env/config and exposes constants (manually created)
│   ├── static\
│   │   └── main.css                 # Simple CSS for UI (manually created)
│   └── templates\
│       └── index.html               # Frontend HTML (manually created)
├── tests\
│   ├── __init__.py                  # package marker for tests (manually created)
│   ├── test_core.py                 # Unit tests for calculator.core (manually created)
│   ├── test_validators.py           # Unit tests for validators (manually created)
│   └── test_api.py                  # Integration tests for API endpoints (manually created)
├── .env.example                     # Example env variables (manually created)
├── requirements.txt                 # Exact pip dependencies (manually created)
├── README.md                        # Project README and usage (manually created)
├── .gitignore                       # .gitignore (manually created)
└── run_dev.bat                      # Windows helper script to run dev server (manually created)
```

Notes on files:
- src/app.py: main Flask app and HTTP endpoints. Manual.
- src/calculator/core.py: Contains Calculator class with arithmetic methods using Decimal. Manual.
- src/calculator/exceptions.py: Custom exceptions for validation and calculation errors. Manual.
- src/calculator/validators.py: Validate input strings and convert to Decimal securely. Manual.
- src/config/settings.py: Loads .env and exposes constants like DECIMAL_PRECISION. Manual.
- static/main.css: Basic styling for index.html. Manual.
- templates/index.html: UI page with form and JS for fetch POST request. Manual.
- requirements.txt: pin versions. Manual.
- tests/*: Manual tests using pytest/pytest-flask.
- run_dev.bat: Simple Windows script to activate venv and run app. Manual.

Auto-generated:
- venv/ directory (created by python -m venv; not included in repo)
- __pycache__ folders (created by Python)
- .pytest_cache (created by pytest)

## 4. DATA MODELS & SCHEMAS (If Applicable)

This is a simple calculator — no persistent data models or database. However, we define internal data shapes (Python dataclasses / types) used in control flow.

Pseudo-models (not persisted):

1) CalculationRequest (not an actual dataclass file but documented)
- operand1: Decimal
  - type: decimal.Decimal
  - constraints: must be a finite Decimal; no NaN or Infinity
- operand2: Decimal
  - type: decimal.Decimal
  - constraints: same as operand1
- operation: str
  - allowed values: "add", "subtract", "multiply", "divide", "+" , "-" , "*" , "/"
  - required

2) CalculationResult
- result: Decimal
  - type: decimal.Decimal
  - representation: JSON will serialize as string to avoid float loss
- operation: str
- operand1: str (original string representation as provided)
- operand2: str
- timestamp: ISO8601 string (generated by API)

Validation rules:
- operand strings must be convertible to Decimal with a context that disallows NaN/Infinity.
- When operation == "divide" or "/" and operand2 == 0: raise DivisionByZeroError.

Default behavior:
- DECIMAL_PRECISION default: 28 (configurable)
- DECIMAL_ROUNDING default: ROUND_HALF_EVEN

## 5. MODULE SPECIFICATIONS (For Each File)

All function signatures include full type hints.

File: src/__init__.py
- Purpose: Package marker; can optionally expose create_app factory.
- Content: from .app import create_app
- Public: create_app() — imported from app module.

File: src/app.py
- Purpose: Create and run Flask application and define endpoints.

Public functions:
- def create_app(config_overrides: dict | None = None) -> "Flask":
  - Parameters:
    - config_overrides: optional dict to override settings for testing.
  - Returns: Flask application instance.
  - Example:
    >>> app = create_app()
    >>> app.test_client().get("/")
- def _json_response(payload: dict, status: int = 200) -> Response (internal helper but available)
  - Purpose: Standardize JSON responses.

Endpoints:
- GET / (index)
  - Renders templates/index.html.
  - Returns: HTML 200.
- POST /api/calculate
  - Request Content-Type: application/json
  - Request body example:
    {
      "operand1": "3.5",
      "operand2": "2",
      "operation": "multiply"
    }
  - Response Success (200):
    {
      "status": "success",
      "data": {
         "operand1": "3.5",
         "operand2": "2",
         "operation": "multiply",
         "result": "7.0",
         "timestamp": "2025-01-01T12:00:00Z"
      }
    }
  - Error Responses:
    - 400 Bad Request:
      {
        "status": "error",
        "error": {
           "code": "validation_error",
           "message": "operand1 is required and must be a numeric value"
        }
      }
    - 400 Division by zero:
      {
        "status": "error",
        "error": {
           "code": "division_by_zero",
           "message": "Cannot divide by zero"
        }
      }

Dependencies:
- imports from src.calculator.core, src.calculator.validators, src.config.settings
- uses flask and flask.jsonify

Error handling:
- Catches calculator exceptions (ValidationError, CalculationError, DivisionByZeroError) and returns appropriate 400 responses.
- On unhandled exceptions, logs full exception and returns 500 with generic message.

File: src/calculator/core.py
- Purpose: Core arithmetic operations, using Decimal, with a small public API.

Public Classes/Functions:

- from decimal import Decimal, getcontext, Context

- class Calculator:
  - Responsibility: Provide static arithmetic methods and a helper to compute based on string inputs and an operation token.
  - Methods:
    - @staticmethod
      def add(a: Decimal, b: Decimal) -> Decimal
      - Returns a + b
    - @staticmethod
      def subtract(a: Decimal, b: Decimal) -> Decimal
      - Returns a - b
    - @staticmethod
      def multiply(a: Decimal, b: Decimal) -> Decimal
      - Returns a * b
    - @staticmethod
      def divide(a: Decimal, b: Decimal) -> Decimal
      - Raises DivisionByZeroError if b == Decimal('0')
      - Returns a / b with Decimal context precision
    - @staticmethod
      def compute(a: Decimal, b: Decimal, operation: str) -> Decimal
      - Allowed operation tokens: "add", "subtract", "multiply", "divide", "+", "-", "*", "/"
      - Internally maps to method and returns Decimal result
  - Example:
    >>> from decimal import Decimal
    >>> Calculator.add(Decimal("1.5"), Decimal("2"))
    Decimal('3.5')

Private Helpers:
- _normalize_operation(operation: str) -> str : converts synonyms to canonical token

Dependencies:
- decimal
- src.calculator.exceptions for exceptions

Error Handling:
- If operation unsupported: raises ValidationError with message "Unsupported operation: {operation}"
- Division by zero handled by divide method raising DivisionByZeroError

File: src/calculator/exceptions.py
- Purpose: Define application-specific exceptions.

Classes:
- class CalculatorError(Exception)
  - Base for all calculator exceptions.
- class ValidationError(CalculatorError)
  - Raised for invalid input/operation.
- class DivisionByZeroError(CalculatorError)
  - Raised when dividing by zero.
- class CalculationError(CalculatorError)
  - Generic calculation failures.

Each exception accepts message: str

File: src/calculator/validators.py
- Purpose: Validate and convert incoming request payloads into Decimal operands and canonical operation token.

Public functions:
- def parse_decimal(value: str) -> Decimal:
  - Parameters: value: str (or numeric)
  - Returns: decimal.Decimal
  - Behavior: 
    - Accept str, int, float; convert to string first, then to Decimal using Decimal(str(value)) for floats to avoid binary floating artifacts.
    - Use Decimal.quantize? No — leave raw; Arithmetic uses context precision for rounding.
    - Validate: not NaN, not Infinity, finite.
    - Raises ValidationError with detail on failure.
  - Example:
    >>> parse_decimal("3.50")
    Decimal('3.50')

- def validate_operation(operation: str) -> str:
  - Parameters: operation: str
  - Returns: canonical operation token: one of "add","subtract","multiply","divide"
  - Accepts synonyms: "+","add","plus","-","subtract","*","multiply","x","times","/","divide"
  - Case-insensitive
  - Raises ValidationError for unsupported operations.

- def validate_request_payload(payload: dict) -> tuple[Decimal, Decimal, str]:
  - Parameters: payload: dict expected keys operand1, operand2, operation
  - Returns: (Decimal operand1, Decimal operand2, canonical operation str)
  - Validates existence and type and uses parse_decimal and validate_operation.
  - Raises ValidationError if missing fields or invalid values.

Dependencies:
- decimal
- src.calculator.exceptions

Error Handling:
- Raise ValidationError for invalid/missing inputs

File: src/config/settings.py
- Purpose: Load environment variables (.env) and expose configuration values.

Public variables:
- DECIMAL_PRECISION: int (default 28)
- DECIMAL_ROUNDING: str (one of decimal rounding constants; default "ROUND_HALF_EVEN")
- DEBUG: bool
- SECRET_KEY: str or None
- LOG_LEVEL: str default "INFO"

Behavior:
- Uses python-dotenv to load .env file if present.
- Example .env keys documented in .env.example.

File: src/templates/index.html
- Purpose: Single page UI form; fetches POST /api/calculate and displays result or error.

Important parts:
- HTML form elements:
  - input#operand1 (text)
  - input#operand2 (text)
  - select#operation or radio buttons for operation
  - button#submit
- JS:
  - performs fetch() POST to /api/calculate with JSON payload
  - disables submit while waiting
  - shows result or error message under result container
  - displays validation errors from API

File: src/static/main.css
- Purpose: Minimal styles for the page.

## 6. API DESIGN

Base URL (development):
- http://127.0.0.1:5000/

Endpoints:

1) GET /
- Purpose: Serve the web UI.
- Request: No body.
- Response: HTML (index.html) with status 200.

2) POST /api/calculate
- Purpose: Compute arithmetic operation for two operands.
- HTTP Method: POST
- Path: /api/calculate
- Request Headers:
  - Content-Type: application/json
- Request Body JSON:
  - operand1: string or number (prefer string to preserve formatting)
  - operand2: string or number
  - operation: string (allowed: "add","subtract","multiply","divide" or symbols "+","-","*","/")
- Example Request:
  {
    "operand1": "3.14",
    "operand2": "2",
    "operation": "multiply"
  }
- Response Codes:
  - 200 OK (success)
    - Response Body:
      {
        "status": "success",
        "data": {
           "operand1": "3.14",
           "operand2": "2",
           "operation": "multiply",
           "result": "6.28",
           "timestamp": "2025-12-06T10:00:00Z"
        }
      }
    - Content-Type: application/json
  - 400 Bad Request (validation error)
    - Response Body:
      {
        "status": "error",
        "error": {
           "code": "validation_error",
           "message": "operand1 is required and must be a numeric value"
        }
      }
  - 400 Bad Request (division by zero)
    - Response Body:
      {
        "status": "error",
        "error": {
           "code": "division_by_zero",
           "message": "Cannot divide by zero"
        }
      }
  - 500 Internal Server Error
    - Response Body:
      {
        "status": "error",
        "error": {
           "code": "server_error",
           "message": "An internal error occurred"
        }
      }

Authentication:
- None required.

Content Negotiation:
- Requests must be application/json for API. UI is regular GET.

Error message consistency:
- All errors return {"status":"error", "error":{"code":..., "message":...}}

Input/output JSON requirements:
- All numeric values in responses are strings to avoid float serialization issues. E.g., "result": "6.28"

## 7. DETAILED IMPLEMENTATION STEPS

The steps are numbered and sequential. Follow them exactly for reproducible setup.

Step 1: Create project directory (if not present)
- Command (Windows PowerShell or cmd):
  - mkdir "C:\Users\balas\Documents\Projects\webcalc2"
  - cd "C:\Users\balas\Documents\Projects\webcalc2"

Step 2: Initialize Git repository (optional)
- git init
- Create .gitignore with at least:
  ```
  venv/
  __pycache__/
  .pytest_cache/
  *.pyc
  .env
  ```

Step 3: Create virtual environment
- Command:
  - python -m venv venv
- Activate:
  - PowerShell: .\venv\Scripts\Activate.ps1
  - cmd.exe: .\venv\Scripts\activate.bat

Step 4: Create requirements.txt
- Create file at C:\Users\balas\Documents\Projects\webcalc2\requirements.txt with exact contents:
  ```
  Flask==2.3.2
  python-dotenv==1.0.0
  pytest==7.4.0
  pytest-flask==1.4.0
  flake8==6.1.0
  black==24.1.0
  ```
- Install:
  - pip install -r requirements.txt

Step 5: Create directory structure and files
- Commands:
  ```
  mkdir src
  mkdir src\calculator
  mkdir src\config
  mkdir src\static
  mkdir src\templates
  mkdir tests
  ```
- Create empty __init__.py files:
  - src\__init__.py
  - src\calculator\__init__.py
  - src\config\__init__.py
  - tests\__init__.py

Step 6: Implement settings module
- File: src\config\settings.py
- Code to write (high-level but clear):
  - Use python-dotenv.load_dotenv() to load .env (or .env default)
  - Read DECIMAL_PRECISION (int) default 28
  - Read DECIMAL_ROUNDING (string): default "ROUND_HALF_EVEN"
  - Read DEBUG (bool) default False
  - Read LOG_LEVEL default "INFO"
  - Example content (exact lines to implement):
    - import os
    - from dotenv import load_dotenv
    - load_dotenv()
    - DECIMAL_PRECISION = int(os.getenv("DECIMAL_PRECISION", "28"))
    - DECIMAL_ROUNDING = os.getenv("DECIMAL_ROUNDING", "ROUND_HALF_EVEN")
    - DEBUG = os.getenv("DEBUG", "False").lower() in ("1", "true", "yes")
    - SECRET_KEY = os.getenv("SECRET_KEY", "change-this-in-production")
    - LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

- Validation checkpoint: run python -c "from src.config import settings; print(settings.DECIMAL_PRECISION)"

Step 7: Implement exceptions
- File: src\calculator\exceptions.py
- Create classes CalculatorError, ValidationError, DivisionByZeroError, CalculationError with docstrings.

Step 8: Implement validators
- File: src\calculator\validators.py
- Implement parse_decimal(value: str|int|float) -> Decimal using Decimal(str(value)) to avoid float repr issues.
- Use decimal.InvalidOperation handling and raise ValidationError with descriptive message.
- Ensure parsed Decimal is finite by using decimal.Decimal.is_finite() (value.is_finite()).
- Implement validate_operation(operation: str) mapping synonyms and raising ValidationError when unsupported.
- Implement validate_request_payload(payload: dict) that ensures keys exist and returns tuple(Decimal, Decimal, canonical_operation).
- Validation checkpoint: Run a small REPL test after writing.

Step 9: Implement core calculator
- File: src\calculator\core.py
- Implement Calculator class as specified.
- Ensure in module top-level, set decimal.getcontext().prec = settings.DECIMAL_PRECISION and rounding accordingly:
  - import decimal
  - from src.config import settings
  - decimal.getcontext().prec = settings.DECIMAL_PRECISION
  - decimal.getcontext().rounding = getattr(decimal, settings.DECIMAL_ROUNDING)
- Implement add/subtract/multiply/divide/compute as specified.
- Raise DivisionByZeroError if attempt to divide by zero.

Step 10: Implement Flask app
- File: src\app.py
- Create create_app factory:
  - app = Flask(__name__, static_folder="static", template_folder="templates")
  - load config into app.config (DEBUG, SECRET_KEY)
  - Add routes GET / and POST /api/calculate
  - POST handler flow:
    1. Read JSON: request.get_json(force=True, silent=False)
    2. validators.validate_request_payload(payload)
    3. result = Calculator.compute(a,b,operation)
    4. Format result as string: str(result.normalize()?) — prefer format to remove exponent if possible. Use str(result)
    5. Return JSON success structure
  - Ensure to catch exceptions and return consistent error responses.
  - Logging: use Python logging module configured to write to file webcalc2.log in project root and console. Use app.logger or logging.getLogger(__name__).

Step 11: Implement HTML UI
- File: src/templates/index.html
- Basic layout:
  - Input fields for operand1, operand2
  - Select box with operations (Add +, Subtract -, Multiply *, Divide /)
  - JS to submit using fetch to /api/calculate
  - Display response messages and handle loading states
- UI test: open browser to http://127.0.0.1:5000/ and try sample calculations.

Step 12: Add CSS
- File: src/static/main.css
- Small layout CSS for form and result output

Step 13: Add run_dev.bat
- Content (exact lines):
  ```
  @echo off
  REM Activate virtual environment and run Flask dev server
  call "%~dp0\venv\Scripts\activate.bat"
  set FLASK_APP=src.app:create_app
  set FLASK_ENV=development
  python -m flask run
  ```
- This helper script assumes venv is in project root.

Step 14: Create .env.example
- Create file with content:
  ```
  # Example environment variables
  DECIMAL_PRECISION=28
  DECIMAL_ROUNDING=ROUND_HALF_EVEN
  DEBUG=True
  SECRET_KEY=change-me
  LOG_LEVEL=INFO
  ```

Step 15: Add README.md
- Document setup, installation commands, usage examples, API examples (see section 11 for exact content).

Step 16: Implement tests (unit & integration)
- File: tests/test_core.py
  - Test functions:
    - test_add_two_decimals()
    - test_subtract_negative_result()
    - test_multiply_by_zero()
    - test_divide_valid()
    - test_divide_by_zero_raises()
- File: tests/test_validators.py
  - Test parse_decimal with strings, ints, floats, invalid strings (e.g. "abc"), "NaN"
- File: tests/test_api.py
  - Use pytest-flask to create test client and test:
    - test_api_calculate_add_success()
    - test_api_calculate_invalid_operand_returns_400()
    - test_api_calculate_division_by_zero_returns_400()
    - test_api_missing_field_returns_400()
- Run tests:
  - pytest -q

Step 17: Lint and format
- Optional: run black . and flake8 to check code style.

Step 18: Run app locally
- Activate venv then:
  - set FLASK_APP=src.app:create_app
  - set FLASK_ENV=development
  - python -m flask run
- Or double-click run_dev.bat

Step 19: Manual verification
- UI manual checks:
  - add 2+3 -> 5
  - multiply 3.14 * 2 -> 6.28
  - divide 1 by 3 -> Decimal precision used, e.g., 0.333333... truncated to context precision
- API call examples (curl):
  - curl -X POST http://127.0.0.1:5000/api/calculate -H "Content-Type: application/json" -d "{\"operand1\":\"3\",\"operand2\":\"2\",\"operation\":\"add\"}"

Step 20: Finalize documentation and commit
- Ensure all files saved and commit to git.

(These 20 steps are the main flow; implementing each file thoroughly should be done according to module specs above. Additional sub-steps exist inside each step, but the above covers explicit creation and validation checkpoints.)

## 8. ERROR HANDLING & VALIDATION

Exception hierarchy:
- src/calculator/exceptions.py
  - CalculatorError(Exception): base class
  - ValidationError(CalculatorError): input or operation invalid
  - DivisionByZeroError(CalculatorError): dividing by zero
  - CalculationError(CalculatorError): general computational problems

Where to validate:
- HTTP layer (src/app.py): Validate presence of JSON and that payload is a dict. Use validators.validate_request_payload which raises ValidationError if any problem.
- validators.parse_decimal: ensures numeric values are convertible to Decimal and finite.
- validators.validate_operation: ensure supported operation token.
- core.divide: ensure non-zero denominator.

Error messages:
- Friendly, concise, actionable. Examples:
  - "operand1 is required and must be a numeric value" (missing or invalid)
  - "Unsupported operation: 'modulo'. Supported operations: add, subtract, multiply, divide"
  - "Cannot divide by zero"
  - "Internal server error" for unhandled exceptions (do not expose stack traces in production)

Logging strategy:
- Configure root logger in app.create_app:
  - Log to console at LOG_LEVEL
  - Log to file C:\Users\balas\Documents\Projects\webcalc2\webcalc2.log with rotating file handler (optional, but simple file is acceptable).
  - INFO level logs for successful requests and operations (operation, operands, result)
  - WARNING level for client errors (validation)
  - ERROR or CRITICAL for unhandled exceptions along with stack trace.
- Never log secrets such as SECRET_KEY.

Recovery mechanisms:
- For validation errors, respond with 400 without crashing.
- For unexpected exceptions inside API handler, catch, log full stack, return 500 with generic message.

Edge handling:
- Division by zero => 400 with code "division_by_zero".
- Invalid JSON => 400 with message "Invalid JSON body".
- Large numbers: Decimal will handle but context precision will limit result; document that output may be rounded to DECIMAL_PRECISION.

## 9. TESTING STRATEGY

Test Framework:
- pytest==7.4.0 and pytest-flask==1.4.0

Test Coverage Target:
- Aim for > 90% coverage for calculator core and validators; full test coverage for API response status codes.

Unit Tests:
- tests/test_core.py
  - test_add_two_decimals(): assert Calculator.add(Decimal("1.1"), Decimal("2.2")) == Decimal("3.3")
  - test_subtract_negative_result(): assert Calculator.subtract(Decimal("1"), Decimal("2")) == Decimal("-1")
  - test_multiply_by_decimal(): assert Calculator.multiply(Decimal("1.5"), Decimal("2")) == Decimal("3.0")
  - test_divide_valid(): for Decimal("1"), Decimal("4") check equals Decimal('0.25')
  - test_divide_by_zero_raises(): check DivisionByZeroError is raised

- tests/test_validators.py
  - test_parse_decimal_from_string()
  - test_parse_decimal_from_int()
  - test_parse_decimal_from_float()
  - test_parse_decimal_invalid_string_raises()
  - test_validate_operation_synonyms()

Integration Tests:
- tests/test_api.py (requires create_app and app.test_client)
  - test_api_calculate_add_success():
    - POST /api/calculate -> expect 200, result "5"
  - test_api_calculate_invalid_operand_returns_400():
    - operand1 = "abc" -> expect 400 with code "validation_error"
  - test_api_calculate_division_by_zero_returns_400()
  - test_api_missing_field_returns_400()

Test Fixtures:
- Use app factory with config_overrides to set DEBUG=False and DECIMAL_PRECISION small for predictable rounding in tests.
- Provide JSON payloads in tests.

Mocking Strategy:
- No external dependencies to mock.
- You can mock decimal.getcontext or settings for tests requiring specific precision by using monkeypatch fixture from pytest.

Edge cases to cover:
- Very long decimal strings
- Inputs with leading/trailing whitespace
- Operation synonyms and case-insensitivity
- JSON with numeric types (int/float) and string types

Running tests:
- Activate venv then:
  - pytest -q
- To run a single test:
  - pytest tests/test_core.py::test_add_two_decimals -q

## 10. CONFIGURATION & ENVIRONMENT

Environment Variables (.env or system env):
- DECIMAL_PRECISION: integer, default 28
- DECIMAL_ROUNDING: string, defaults to ROUND_HALF_EVEN. Valid values: ROUND_HALF_EVEN, ROUND_HALF_UP, ROUND_HALF_DOWN, ROUND_FLOOR, ROUND_CEILING, ROUND_DOWN, ROUND_UP
- DEBUG: boolean (True/False) default False
- SECRET_KEY: string (used by Flask; default provided but change in production)
- LOG_LEVEL: e.g. INFO, DEBUG, WARNING, ERROR

Example .env (file: .env.example)
```
DECIMAL_PRECISION=28
DECIMAL_ROUNDING=ROUND_HALF_EVEN
DEBUG=True
SECRET_KEY=change-this
LOG_LEVEL=INFO
```

Default Values:
- DECIMAL_PRECISION: 28
- DECIMAL_ROUNDING: ROUND_HALF_EVEN
- DEBUG: False
- LOG_LEVEL: INFO

Secrets Management:
- SECRET_KEY should not be committed. Use system secret management for production. .env should be in .gitignore.

Configuration Loading:
- src/config/settings.py uses python-dotenv to load .env and os.getenv with defaults.

## 11. USAGE EXAMPLES & DOCUMENTATION

Installation steps (Windows):

1. Clone repo (if using git):
   - git clone <repo-url> "C:\Users\balas\Documents\Projects\webcalc2"
2. Enter project directory:
   - cd "C:\Users\balas\Documents\Projects\webcalc2"
3. Create virtual environment:
   - python -m venv venv
4. Activate:
   - .\venv\Scripts\Activate.ps1 (PowerShell) or .\venv\Scripts\activate.bat (cmd)
5. Install dependencies:
   - pip install -r requirements.txt
6. Copy .env.example to .env and edit if needed:
   - copy .env.example .env
   - (Edit file) not mandatory for default values.
7. Run dev server:
   - set FLASK_APP=src.app:create_app
   - set FLASK_ENV=development
   - python -m flask run
   - Or double-click run_dev.bat

Basic Usage Example (UI):
- Open browser: http://127.0.0.1:5000/
- Enter operand1 = 3.5, operand2 = 2, operation = multiply -> click Calculate
- Expected displayed output: "Result: 7.0"

API usage (curl examples):
- Add:
  - curl -s -X POST http://127.0.0.1:5000/api/calculate -H "Content-Type: application/json" -d "{\"operand1\": \"3\", \"operand2\": \"2\", \"operation\": \"add\"}"
  - Response:
    {
      "status":"success",
      "data": {"operand1":"3","operand2":"2","operation":"add","result":"5","timestamp":"2025-12-06T10:00:00Z"}
    }
- Division by zero:
  - Request with operand2 "0" and operation "divide"
  - Response code 400 and:
    {"status":"error","error":{"code":"division_by_zero","message":"Cannot divide by zero"}}

Expected output samples:
- Input: operand1=1.5, operand2=2, operation=add => result "3.5"
- Input: operand1=1, operand2=3, operation=divide => result consistent with DECIMAL_PRECISION

## 12. EDGE CASES & CONSIDERATIONS

Known Limitations:
- No persistence. Each request stateless.
- UI is minimalistic and not optimized for mobile.
- No authentication. API is open on host.
- Decimal context precision limits very large or recurring decimals; results truncated/rounded accordingly.

Performance Considerations:
- CPU and memory usage negligible for arithmetic ops. Not designed for bulk/batch operations.
- For very high concurrency or heavy usage, consider WSGI server (gunicorn) and deployment to proper infrastructure.

Security Considerations:
- Input validation prevents code injection as raw inputs are treated as strings and parsed to Decimal.
- Avoid reflecting raw inputs back to HTML without escaping (Jinja autoescapes, but JS must display safely).
- Do not expose SECRET_KEY or stack traces in production; ensure DEBUG False.
- Rate-limiting not implemented; if exposed publicly, consider adding rate-limiting.

Scalability:
- For growth, split UI and API, deploy behind a WSGI server, add load balancing.
- For analytics or logs aggregation, forward logs to centralized logging.

Edge Cases to Handle:
- Very large numeric strings: Decimal will parse but may exceed context precision — handle via rounding and inform user via documentation.
- Input with trailing/leading whitespace: validators should strip whitespace.
- Inputs like "NaN" or "Infinity": validators should reject as not finite.
- Floats: converting floats to Decimal using str(value) to avoid floating binary artifacts.
- Non-JSON POSTs: return 400 "Invalid JSON body".

## EXAMPLE FILE CONTENTS (Core files — minimal but detailed code guidance)

Below are exact pseudo/actual content suggestions for main files. Developer may copy/paste into files.

1) src/config/settings.py (exact content recommended):

```python
# src/config/settings.py
import os
from dotenv import load_dotenv

load_dotenv()  # loads .env from project root if present

DECIMAL_PRECISION = int(os.getenv("DECIMAL_PRECISION", "28"))
DECIMAL_ROUNDING = os.getenv("DECIMAL_ROUNDING", "ROUND_HALF_EVEN")
DEBUG = os.getenv("DEBUG", "False").lower() in ("1", "true", "yes")
SECRET_KEY = os.getenv("SECRET_KEY", "change-this-in-production")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
```

2) src/calculator/exceptions.py

```python
# src/calculator/exceptions.py

class CalculatorError(Exception):
    """Base exception for calculator errors."""

class ValidationError(CalculatorError):
    """Raised when input validation fails."""

class DivisionByZeroError(CalculatorError):
    """Raised when dividing by zero."""

class CalculationError(CalculatorError):
    """Raised for general calculation failures."""
```

3) src/calculator/validators.py

```python
# src/calculator/validators.py
from decimal import Decimal, InvalidOperation
from typing import Tuple
from .exceptions import ValidationError

_OPERATION_MAP = {
    "add": "add", "+": "add", "plus": "add",
    "subtract": "subtract", "-": "subtract", "minus": "subtract",
    "multiply": "multiply", "*": "multiply", "x": "multiply", "times": "multiply",
    "divide": "divide", "/": "divide",
}

def parse_decimal(value) -> Decimal:
    """Parse value into Decimal, raising ValidationError on failure."""
    if value is None:
        raise ValidationError("Numeric value is required")
    # Accept numbers and strings; convert to str first
    try:
        s = str(value).strip()
        d = Decimal(s)
    except (InvalidOperation, ValueError):
        raise ValidationError(f"Invalid numeric value: '{value}'")
    # check finite
    if not d.is_finite():
        raise ValidationError(f"Numeric value must be finite: '{value}'")
    return d

def validate_operation(op: str) -> str:
    if op is None:
        raise ValidationError("Operation is required")
    key = str(op).strip().lower()
    if key in _OPERATION_MAP:
        return _OPERATION_MAP[key]
    raise ValidationError(f"Unsupported operation: '{op}'. Supported: add, subtract, multiply, divide")

def validate_request_payload(payload: dict) -> Tuple[Decimal, Decimal, str]:
    if not isinstance(payload, dict):
        raise ValidationError("JSON object expected")
    if "operand1" not in payload:
        raise ValidationError("operand1 is required")
    if "operand2" not in payload:
        raise ValidationError("operand2 is required")
    if "operation" not in payload:
        raise ValidationError("operation is required")
    a = parse_decimal(payload["operand1"])
    b = parse_decimal(payload["operand2"])
    op = validate_operation(payload["operation"])
    return a, b, op
```

4) src/calculator/core.py

```python
# src/calculator/core.py
from decimal import Decimal, getcontext, ROUND_HALF_EVEN
from typing import Callable
from src.config import settings
from .exceptions import DivisionByZeroError, ValidationError

# configure decimal context
ctx = getcontext()
ctx.prec = settings.DECIMAL_PRECISION
ctx.rounding = getattr(__import__('decimal'), settings.DECIMAL_ROUNDING, ROUND_HALF_EVEN)

class Calculator:
    @staticmethod
    def add(a: Decimal, b: Decimal) -> Decimal:
        return a + b

    @staticmethod
    def subtract(a: Decimal, b: Decimal) -> Decimal:
        return a - b

    @staticmethod
    def multiply(a: Decimal, b: Decimal) -> Decimal:
        return a * b

    @staticmethod
    def divide(a: Decimal, b: Decimal) -> Decimal:
        if b == Decimal("0"):
            raise DivisionByZeroError("Cannot divide by zero")
        return a / b

    @staticmethod
    def compute(a: Decimal, b: Decimal, operation: str) -> Decimal:
        op = operation.lower()
        if op == "add":
            return Calculator.add(a, b)
        if op == "subtract":
            return Calculator.subtract(a, b)
        if op == "multiply":
            return Calculator.multiply(a, b)
        if op == "divide":
            return Calculator.divide(a, b)
        raise ValidationError(f"Unsupported operation: {operation}")
```

5) src/app.py

```python
# src/app.py
import logging
from datetime import datetime, timezone
from flask import Flask, request, jsonify, render_template
from src.calculator.validators import validate_request_payload
from src.calculator.core import Calculator
from src.calculator.exceptions import CalculatorError, ValidationError, DivisionByZeroError
from src.config import settings
import os

def create_app(config_overrides: dict | None = None) -> Flask:
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config["DEBUG"] = settings.DEBUG
    app.config["SECRET_KEY"] = settings.SECRET_KEY

    # Logging setup
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    handler.setLevel(log_level)
    app.logger.setLevel(log_level)
    app.logger.addHandler(handler)

    # also log to file
    file_handler = logging.FileHandler(os.path.join(os.path.dirname(__file__), "..", "webcalc2.log"))
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)

    if config_overrides:
        app.config.update(config_overrides)

    @app.route("/", methods=["GET"])
    def index():
        return render_template("index.html")

    @app.route("/api/calculate", methods=["POST"])
    def api_calculate():
        try:
            payload = request.get_json(force=True)
        except Exception as exc:
            app.logger.warning("Invalid JSON body: %s", exc)
            return jsonify({"status": "error", "error": {"code": "invalid_json", "message": "Invalid JSON body"}}), 400

        try:
            a, b, op = validate_request_payload(payload)
            app.logger.info("Request: %s %s %s", a, op, b)
            result = Calculator.compute(a, b, op)
            # Return result as string to preserve decimal representation
            data = {
                "operand1": str(a),
                "operand2": str(b),
                "operation": op,
                "result": format(result, "f"),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            app.logger.info("Result: %s", data["result"])
            return jsonify({"status": "success", "data": data}), 200
        except DivisionByZeroError as ex:
            app.logger.warning("Division by zero: %s", ex)
            return jsonify({"status": "error", "error": {"code": "division_by_zero", "message": str(ex)}}), 400
        except ValidationError as ex:
            app.logger.warning("Validation error: %s", ex)
            return jsonify({"status": "error", "error": {"code": "validation_error", "message": str(ex)}}), 400
        except CalculatorError as ex:
            app.logger.error("Calculator error: %s", ex)
            return jsonify({"status": "error", "error": {"code": "calculation_error", "message": str(ex)}}), 400
        except Exception as ex:
            app.logger.exception("Unhandled exception while computing")
            return jsonify({"status": "error", "error": {"code": "server_error", "message": "An internal error occurred"}}), 500

    return app
```

6) src/templates/index.html (important parts):

```html
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>WebCalc2 - Simple Calculator</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="/static/main.css">
</head>
<body class="container py-4">
  <h1>WebCalc2 - Simple Calculator</h1>
  <form id="calcForm" class="mb-3">
    <div class="mb-2">
      <label for="operand1">Operand 1</label>
      <input id="operand1" name="operand1" class="form-control" type="text" placeholder="e.g. 3.14" required />
    </div>
    <div class="mb-2">
      <label for="operand2">Operand 2</label>
      <input id="operand2" name="operand2" class="form-control" type="text" placeholder="e.g. 2" required />
    </div>
    <div class="mb-2">
      <label for="operation">Operation</label>
      <select id="operation" name="operation" class="form-select">
        <option value="add">Add (+)</option>
        <option value="subtract">Subtract (-)</option>
        <option value="multiply">Multiply (*)</option>
        <option value="divide">Divide (/)</option>
      </select>
    </div>
    <button id="submit" class="btn btn-primary" type="submit">Calculate</button>
  </form>

  <div id="result" class="alert d-none" role="alert"></div>

  <script>
    const form = document.getElementById('calcForm');
    const resultEl = document.getElementById('result');

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      resultEl.classList.add('d-none');
      const payload = {
        operand1: document.getElementById('operand1').value,
        operand2: document.getElementById('operand2').value,
        operation: document.getElementById('operation').value
      };
      document.getElementById('submit').disabled = true;
      try {
        const resp = await fetch('/api/calculate', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify(payload)
        });
        const json = await resp.json();
        if (resp.ok && json.status === 'success') {
          resultEl.className = 'alert alert-success';
          resultEl.textContent = `Result: ${json.data.result}`;
        } else {
          resultEl.className = 'alert alert-danger';
          resultEl.textContent = json.error?.message || 'An error occurred';
        }
      } catch (err) {
        resultEl.className = 'alert alert-danger';
        resultEl.textContent = 'Network error: ' + err.message;
      } finally {
        resultEl.classList.remove('d-none');
        document.getElementById('submit').disabled = false;
      }
    });
  </script>
</body>
</html>
```

7) src/static/main.css (simple)

```css
body { max-width: 680px; margin: 0 auto; }
```

8) tests/test_core.py (example tests)

```python
# tests/test_core.py
from decimal import Decimal
from src.calculator.core import Calculator
import pytest
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
```

9) tests/test_api.py (integration examples)

```python
# tests/test_api.py
import json
import pytest
from src.app import create_app
from src.config import settings

@pytest.fixture
def app():
    # override settings for tests
    app = create_app({"TESTING": True})
    return app

def test_api_calculate_add_success(client):
    resp = client.post("/api/calculate", json={"operand1": "3", "operand2": "2", "operation": "add"})
    assert resp.status_code == 200
    j = resp.get_json()
    assert j["status"] == "success"
    assert j["data"]["result"] == "5"

def test_api_invalid_operand_returns_400(client):
    resp = client.post("/api/calculate", json={"operand1": "abc", "operand2": "2", "operation": "add"})
    assert resp.status_code == 400
    j = resp.get_json()
    assert j["status"] == "error"
    assert j["error"]["code"] == "validation_error"

def test_api_divide_by_zero(client):
    resp = client.post("/api/calculate", json={"operand1": "1", "operand2": "0", "operation": "divide"})
    assert resp.status_code == 400
    j = resp.get_json()
    assert j["error"]["code"] == "division_by_zero"
```

## QUALITY CHECKLIST (double-check before implementation)

- [x] All file names are explicit as above, exact path rooted under C:\Users\balas\Documents\Projects\webcalc2
- [x] All library versions specified in requirements.txt
- [x] All function signatures in spec include type hints
- [x] Module purposes are clearly stated
- [x] Implementation steps are numbered and sequential (20+ steps)
- [x] Error handling specified for each critical function and API
- [x] Test cases are concrete and named
- [x] Configuration examples (.env.example) provided
- [x] README and usage examples included
- [x] No vague placeholders: concrete code snippets and behavior specified

## IMPLEMENTATION NOTES, TIPS & PITFALLS

- Use Decimal with string conversion: Decimal(str(float_val)) is safe; better to accept strings.
- Converting Python float directly to Decimal may produce unexpected binary artifacts. Prefer accepting string input from UI.
- Always normalize displayed Decimal via format(result, "f") to remove exponent notation for user-friendly display.
- For rounding/truncation expectations, document DECIMAL_PRECISION. Tests should use small precision if needed.
- For production readiness, set DEBUG=False and configure allowed hosts / reverse proxy / SSL.

## FINAL REMARKS

This specification provides a complete, implementable blueprint for a simple web calculator supporting addition, subtraction, multiplication, and division. It includes a web UI and JSON API, thorough validation and error handling, Decimal arithmetic for precision, tests, logging, and configuration via environment variables. Follow each file and step exactly under C:\Users\balas\Documents\Projects\webcalc2 to implement the project without further clarifications.