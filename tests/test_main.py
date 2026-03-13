import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_home():
    """Test the home page loads correctly."""
    response = client.get("/home")
    assert response.status_code == 200
    assert "Sashanator!" in response.text
    assert response.headers["content-type"] == "text/html; charset=utf-8"

def test_home_page_style():
    """Test that the home page has the correct style."""
    response = client.get("/home")
    assert response.status_code == 200
    assert '<body style="background-color: #FF0000;' in response.text