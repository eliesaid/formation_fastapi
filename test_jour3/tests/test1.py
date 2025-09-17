from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_info_route():
    response = client.get("/info")
    assert response.status_code == 200
    data = response.json()
    assert data["version"] == "1.0"
    assert "app" in data

# pytest test1.py