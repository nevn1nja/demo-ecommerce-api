def test_read_products_valid_pagination(mock_db, client):
    response = client.get("/products/?skip=0&limit=10")
    assert response.status_code == 200
    assert "data" in response.json()
    assert "meta" in response.json()
    assert len(response.json()["data"]) <= 10

def test_read_products_invalid_skip(mock_db, client):
    response = client.get("/products/?skip=-1&limit=10")
    assert response.status_code == 422

def test_read_products_invalid_limit(mock_db, client):
    response = client.get("/products/?skip=0&limit=1001")
    assert response.status_code == 422

def test_read_products_invalid_limit_zero(mock_db, client):
    response = client.get("/products/?skip=0&limit=0")
    assert response.status_code == 422
    assert response.json()["detail"] == "Limit must be between 1 and 1000."

def test_create_product_valid(mock_db, client):
    product_payload = {"name": "Test Product", "description": "A description", "price": 19.99, "stock": 100}
    response = client.post("/products/", json=product_payload)
    assert response.status_code == 201
    assert "id" in response.json()
    assert response.json()["name"] == "Test Product"
    assert response.json()["price"] == 19.99
    assert response.json()["stock"] == 100


