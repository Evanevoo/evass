import pytest
from fastapi import status
from datetime import datetime, timedelta

def test_create_cylinder_movement(client, test_token, test_cylinder, test_location):
    headers = {"Authorization": f"Bearer {test_token}"}
    movement_data = {
        "cylinder_id": test_cylinder.id,
        "from_location_id": None,  # From warehouse
        "to_location_id": test_location.id,
        "movement_type": "delivery",
        "notes": "Test delivery"
    }
    response = client.post(
        "/api/movements/cylinder",
        headers=headers,
        json=movement_data
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["cylinder_id"] == test_cylinder.id
    assert data["to_location_id"] == test_location.id
    assert data["movement_type"] == "delivery"

def test_create_cylinder_movement_unauthorized(client, test_cylinder, test_location):
    movement_data = {
        "cylinder_id": test_cylinder.id,
        "from_location_id": None,
        "to_location_id": test_location.id,
        "movement_type": "delivery",
        "notes": "Test delivery"
    }
    response = client.post(
        "/api/movements/cylinder",
        json=movement_data
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_create_cylinder_movement_invalid_cylinder(client, test_token, test_location):
    headers = {"Authorization": f"Bearer {test_token}"}
    movement_data = {
        "cylinder_id": 999,
        "from_location_id": None,
        "to_location_id": test_location.id,
        "movement_type": "delivery",
        "notes": "Test delivery"
    }
    response = client.post(
        "/api/movements/cylinder",
        headers=headers,
        json=movement_data
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_get_cylinder_movements(client, test_token):
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get("/api/movements/cylinder", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "cylinder_id" in data[0]
    assert "movement_type" in data[0]

def test_get_cylinder_movement_history(client, test_token, test_cylinder):
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get(
        f"/api/movements/cylinder/{test_cylinder.id}",
        headers=headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["cylinder_id"] == test_cylinder.id

def test_create_transaction(client, test_token, test_customer, test_cylinder):
    headers = {"Authorization": f"Bearer {test_token}"}
    transaction_data = {
        "customer_id": test_customer.id,
        "transaction_type": "sale",
        "items": [
            {
                "cylinder_id": test_cylinder.id,
                "quantity": 1,
                "unit_price": 100.00
            }
        ]
    }
    response = client.post(
        "/api/movements/transaction",
        headers=headers,
        json=transaction_data
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["customer_id"] == test_customer.id
    assert data["transaction_type"] == "sale"
    assert data["total_amount"] == 100.00
    assert len(data["items"]) == 1
    assert data["items"][0]["cylinder_id"] == test_cylinder.id

def test_create_transaction_unauthorized(client, test_customer, test_cylinder):
    transaction_data = {
        "customer_id": test_customer.id,
        "transaction_type": "sale",
        "items": [
            {
                "cylinder_id": test_cylinder.id,
                "quantity": 1,
                "unit_price": 100.00
            }
        ]
    }
    response = client.post(
        "/api/movements/transaction",
        json=transaction_data
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_create_transaction_invalid_customer(client, test_token, test_cylinder):
    headers = {"Authorization": f"Bearer {test_token}"}
    transaction_data = {
        "customer_id": 999,
        "transaction_type": "sale",
        "items": [
            {
                "cylinder_id": test_cylinder.id,
                "quantity": 1,
                "unit_price": 100.00
            }
        ]
    }
    response = client.post(
        "/api/movements/transaction",
        headers=headers,
        json=transaction_data
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_get_transactions(client, test_token):
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get("/api/movements/transaction", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "customer_id" in data[0]
    assert "transaction_type" in data[0]
    assert "total_amount" in data[0]

def test_get_transaction(client, test_token, test_transaction):
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get(
        f"/api/movements/transaction/{test_transaction.id}",
        headers=headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == test_transaction.id
    assert "customer_id" in data
    assert "items" in data

def test_get_nonexistent_transaction(client, test_token):
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get(
        "/api/movements/transaction/999",
        headers=headers
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_complete_transaction(client, test_token, test_transaction):
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.put(
        f"/api/movements/transaction/{test_transaction.id}/complete",
        headers=headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "completed"
    assert "completed_at" in data

def test_complete_transaction_unauthorized(client, test_transaction):
    response = client.put(
        f"/api/movements/transaction/{test_transaction.id}/complete"
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_complete_nonexistent_transaction(client, test_token):
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.put(
        "/api/movements/transaction/999/complete",
        headers=headers
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND 