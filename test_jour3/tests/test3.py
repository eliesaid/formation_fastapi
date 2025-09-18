from fastapi.testclient import TestClient
from main_products import app

client = TestClient(app)

def test_create_product_invalid_price():
    response = client.post("/products/", json={"name": "Sac", "price": "gratuit"})
    assert response.status_code == 422  # Erreur de validation

