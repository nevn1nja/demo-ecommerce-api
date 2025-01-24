from unittest.mock import MagicMock
import logging

def test_create_order_success(mock_db, client):
    product_payload = {
        "name": "item1",
        "description": "desc",
        "price": 1.0,
        "stock": 10,
    }
    response = client.post("/products/", json=product_payload)
    assert response.status_code == 201


