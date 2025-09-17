from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_info_route():
    response = client.get("/info")
    assert response.status_code == 200
    data = response.json()
    assert data["version"] == "1.0"

# Exemple 2 avec main:

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_product():
    response = client.post("/products/", json={"name": "Chaussures", "price": 59.99})
    assert response.status_code == 200
    assert response.json()["product"]["name"] == "Chaussures«

# Exemple 3 : Tester des erreurs

def test_create_product_invalid_price():
    response = client.post("/products/", json={"name": "Sac", "price": "gratuit"})
    assert response.status_code == 422  # Erreur de validation
