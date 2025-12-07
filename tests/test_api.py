"""Integration tests for the Flask API endpoints."""
import pytest
from src.app import create_app


@pytest.fixture
def app():
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


def test_api_divide_by_zero_returns_400(client):
    resp = client.post("/api/calculate", json={"operand1": "1", "operand2": "0", "operation": "divide"})
    assert resp.status_code == 400
    j = resp.get_json()
    assert j["error"]["code"] == "division_by_zero"


def test_api_missing_field_returns_400(client):
    resp = client.post("/api/calculate", json={"operand1": "1", "operation": "add"})
    assert resp.status_code == 400
    j = resp.get_json()
    assert j["error"]["code"] == "validation_error"
