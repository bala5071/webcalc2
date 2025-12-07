# WebCalc2 — Simple Decimal Calculator

🧮 WebCalc2 is a lightweight web application and JSON API that performs the four basic arithmetic operations (addition, subtraction, multiplication, division) using Python's Decimal type to provide precise, deterministic decimal arithmetic.

Key features
- ✅ Web UI (single-page) for interactive usage
- ✅ JSON API endpoint (/api/calculate) for programmatic access
- ✅ Robust input validation with descriptive error responses
- ✅ Accurate Decimal arithmetic with configurable precision and rounding
- ✅ Unit and integration tests (pytest + pytest-flask)
- ✅ Logging to console and project log file

Technology stack
- Python 3.11.6
- Flask==2.3.2
- python-dotenv==1.0.0
- pytest==7.4.0
- pytest-flask==1.4.0
- flake8==6.1.0 (dev)
- black==24.1.0 (dev)

System requirements
- Windows, macOS or Linux with Python 3.11.6 installed
- Recommended: create and use a virtual environment (venv)

Quick start (Windows)
1. Open cmd or PowerShell
2. cd "C:\Users\balas\Documents\Projects\webcalc2"
3. python -m venv venv
4. PowerShell: .\\venv\\Scripts\\Activate.ps1  OR  cmd: .\\venv\\Scripts\\activate.bat
5. pip install -r requirements.txt
6. copy .env.example .env
7. set FLASK_APP=src.app:create_app
8. set FLASK_ENV=development
9. python -m flask run

Or run the provided run_dev.bat (assumes venv is present):
- run_dev.bat

Configuration
- COPY `.env.example` to `.env` and adjust values as needed.
- Available env vars:
  - DECIMAL_PRECISION (int, default 28)
  - DECIMAL_ROUNDING (string, default ROUND_HALF_EVEN)
  - DEBUG (True/False)
  - SECRET_KEY (Flask secret key)
  - LOG_LEVEL (INFO/DEBUG/etc.)

API Usage
- Endpoint: POST /api/calculate
- Content-Type: application/json
- Body: {"operand1": "3.14", "operand2": "2", "operation": "multiply"}
- Successful response (200):
  {
    "status": "success",
    "data": {"operand1": "3.14", "operand2": "2", "operation": "multiply", "result": "6.28", "timestamp": "..."}
  }
- Error responses return 400 or 500 with structure: {"status":"error","error":{"code":"...","message":"..."}}

Examples
- curl example:
  curl -X POST http://127.0.0.1:5000/api/calculate -H "Content-Type: application/json" -d "{\"operand1\": \"3\", \"operand2\": \"2\", \"operation\": \"add\"}"

Testing
- Activate venv
- pip install -r requirements.txt
- pytest -q

Project structure
```
C:\Users\balas\Documents\Projects\webcalc2\
├── src\
│   ├── __init__.py
│   ├── app.py
│   ├── calculator\
│   │   ├── __init__.py
│   │   ├── core.py
│   │   ├── exceptions.py
│   │   └── validators.py
│   ├── config\
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── static\
│   │   └── main.css
│   └── templates\
│       └── index.html
├── tests\
│   ├── __init__.py
│   ├── test_core.py
│   ├── test_validators.py
│   └── test_api.py
├── requirements.txt
├── .env.example
├── .gitignore
└── run_dev.bat
```

Security
- Do not commit `.env` or `SECRET_KEY` values. Use secure secret management in production.
- Set DEBUG=False in production.

Contributing
- See CONTRIBUTING.md for contributor guidelines.

License
- MIT (see LICENSE in repository if added)

Credits
- Built with Flask and Python Decimal for deterministic arithmetic precision.
