import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_home():
    """Test the home page response and content."""
    response = client.get("/home")
    assert response.status_code == 200
    assert "Sashanator!" in response.text
    assert response.text.count('<h1>Sashanator!</h1>') == 1  # Check for prominent text
    assert response.headers['content-type'] == 'text/html; charset=utf-8'