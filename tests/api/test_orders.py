def test_create_order_success(mock_db, client):
    """First we ensure that there is atleast one product in the DB"""
    product_payload = {"name": "item1", "description": "desc", "price": 1.0, "stock": 10, }
    product_response = client.post("/products/", json=product_payload)
    assert product_response.status_code == 201

    order_payload = {"items": [{"product_id": 1, "quantity": 1}]}
    order_response = client.post("/orders/", json=order_payload)
    assert order_response.status_code == 201


def test_create_order_invalid_stock(mock_db, client):
    order_payload = {"items": [{"product_id": 1, "quantity": 10000}]}
    order_response = client.post("/orders/", json=order_payload)
    assert order_response.status_code == 422


def test_create_order_invalid_product_id(mock_db, client):
    order_payload = {"items": [{"product_id": 1000, "quantity": 1}]}
    order_response = client.post("/orders/", json=order_payload)
    assert order_response.status_code == 422
