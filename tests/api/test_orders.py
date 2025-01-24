def test_create_order_success(mock_db, client):
    """First we ensure that there is atleast one product in the DB"""
    item_price = 10.0
    product_payload = {"name": "item1", "description": "desc", "price": item_price, "stock": 10, }
    product_response = client.post("/products/", json=product_payload)
    assert product_response.status_code == 201

    order_quantity = 3
    product = product_response.json()
    order_payload = {"items": [{"product_id": product['id'], "quantity": order_quantity}]}
    order_response = client.post("/orders/", json=order_payload)
    assert order_response.status_code == 201
    expected_total_price = item_price * order_quantity
    assert order_response.json()["total_price"] == expected_total_price


def test_create_order_insufficient_stock(mock_db, client):
    order_payload = {"items": [{"product_id": 1, "quantity": 10000}]}
    order_response = client.post("/orders/", json=order_payload)
    assert order_response.status_code == 422


def test_create_order_invalid_quantity_zero(mock_db, client):
    order_payload = {"items": [{"product_id": 1, "quantity": 0}]}
    order_response = client.post("/orders/", json=order_payload)
    assert order_response.status_code == 422
    assert order_response.json()["detail"] == "Quantity must be greater than zero."


def test_create_order_invalid_quantity_negative(mock_db, client):
    order_payload = {"items": [{"product_id": 1, "quantity": -1}]}
    order_response = client.post("/orders/", json=order_payload)
    assert order_response.status_code == 422
    assert order_response.json()["detail"] == "Quantity must be greater than zero."


def test_create_order_multiple_items(mock_db, client):
    item_price_1 = 10.0
    product_payload_1 = {"name": "item1", "description": "desc1", "price": item_price_1, "stock": 10}
    product1_response = client.post("/products/", json=product_payload_1)

    item_price_2 = 20.0
    product_payload_2 = {"name": "item2", "description": "desc2", "price": item_price_2, "stock": 5}
    product2_response = client.post("/products/", json=product_payload_2)

    product1 = product1_response.json()
    product2 = product2_response.json()
    product1_quantity = 2
    product2_quantity = 1
    order_payload = {"items": [{"product_id": product1['id'], "quantity": product1_quantity},
                               {"product_id": product2['id'], "quantity": product2_quantity}]}
    order_response = client.post("/orders/", json=order_payload)
    assert order_response.status_code == 201
    expected_total_price = (item_price_1 * product1_quantity) + (item_price_2 * product2_quantity)
    assert order_response.json()["total_price"] == expected_total_price


def test_create_order_no_items(mock_db, client):
    order_payload = {"items": []}
    order_response = client.post("/orders/", json=order_payload)
    assert order_response.status_code == 422
    assert order_response.json()["detail"] == "Order must contain at least one item."


def test_create_order_invalid_product_id(mock_db, client):
    order_payload = {"items": [{"product_id": 1000, "quantity": 1}]}
    order_response = client.post("/orders/", json=order_payload)
    assert order_response.status_code == 422


def test_create_order_missing_fields(mock_db, client):
    order_payload = {"items": [{"product_id": None, "quantity": None}]}
    order_response = client.post("/orders/", json=order_payload)
    assert order_response.status_code == 422


def test_create_order_invalid_product_id_type(mock_db, client):
    order_payload = {"items": [{"product_id": "abc", "quantity": 1}]}
    order_response = client.post("/orders/", json=order_payload)
    assert order_response.status_code == 422


def test_create_order_missing_items(mock_db, client):
    order_payload = {}
    order_response = client.post("/orders/", json=order_payload)
    assert order_response.status_code == 422
    assert order_response.json()["detail"] == "Order must contain at least one item."


def test_create_order_missing_quantity(mock_db, client):
    product_payload = {"name": "item1", "description": "desc", "price": 10.0, "stock": 10}
    product_response = client.post("/products/", json=product_payload)
    assert product_response.status_code == 201

    order_payload = {"items": [{"product_id": 1}]}
    order_response = client.post("/orders/", json=order_payload)
    assert order_response.status_code == 422
