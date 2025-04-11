import pytest
from fastapi import status

def test_create_cylinder(client, test_token, test_customer, test_location):
    headers = {"Authorization": f"Bearer {test_token}"}
    cylinder_data = {
        "serial_number": "NEW123",
        "type": "industrial",
        "capacity": 50.0,
        "pressure_rating": 200.0,
        "tare_weight": 30.0,
        "manufacture_date": "2023-01-01",
        "current_customer_id": test_customer.id,
        "current_location_id": test_location.id
    }
    response = client.post("/api/cylinders/", headers=headers, json=cylinder_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["serial_number"] == cylinder_data["serial_number"]
    assert data["type"] == cylinder_data["type"]
    assert data["barcode"] is not None
    assert data["qr_code"] is not None

def test_create_cylinder_unauthorized(client, test_customer, test_location):
    cylinder_data = {
        "serial_number": "NEW123",
        "type": "industrial",
        "capacity": 50.0,
        "pressure_rating": 200.0,
        "tare_weight": 30.0,
        "manufacture_date": "2023-01-01",
        "current_customer_id": test_customer.id,
        "current_location_id": test_location.id
    }
    response = client.post("/api/cylinders/", json=cylinder_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_cylinders(client, test_token):
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get("/api/cylinders/", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "serial_number" in data[0]
    assert "type" in data[0]

def test_get_cylinder_by_id(client, test_token, test_cylinder):
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get(f"/api/cylinders/{test_cylinder.id}", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["serial_number"] == test_cylinder.serial_number
    assert data["type"] == test_cylinder.type

def test_get_nonexistent_cylinder(client, test_token):
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get("/api/cylinders/999", headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_cylinder(client, test_token, test_cylinder):
    headers = {"Authorization": f"Bearer {test_token}"}
    update_data = {
        "type": "medical",
        "capacity": 60.0,
        "pressure_rating": 250.0
    }
    response = client.put(
        f"/api/cylinders/{test_cylinder.id}",
        headers=headers,
        json=update_data
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["type"] == update_data["type"]
    assert data["capacity"] == update_data["capacity"]
    assert data["pressure_rating"] == update_data["pressure_rating"]

def test_update_cylinder_unauthorized(client, test_cylinder):
    update_data = {
        "type": "medical",
        "capacity": 60.0,
        "pressure_rating": 250.0
    }
    response = client.put(
        f"/api/cylinders/{test_cylinder.id}",
        json=update_data
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_delete_cylinder(client, test_token, test_cylinder):
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.delete(f"/api/cylinders/{test_cylinder.id}", headers=headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verify cylinder is deleted
    response = client.get(f"/api/cylinders/{test_cylinder.id}", headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_cylinder_unauthorized(client, test_cylinder):
    response = client.delete(f"/api/cylinders/{test_cylinder.id}")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_cylinder_qr_code(client, test_token, test_cylinder):
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get(f"/api/cylinders/{test_cylinder.id}/qr-code", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["content-type"] == "image/png"

def test_search_cylinder_by_serial(client, test_token, test_cylinder):
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get(f"/api/cylinders/search/{test_cylinder.serial_number}", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["serial_number"] == test_cylinder.serial_number

def test_search_cylinder_by_barcode(client, test_token, test_cylinder):
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get(f"/api/cylinders/search/{test_cylinder.barcode}", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["barcode"] == test_cylinder.barcode

def test_search_nonexistent_cylinder(client, test_token):
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get("/api/cylinders/search/NONEXISTENT", headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND 