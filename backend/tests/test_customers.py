import pytest
from fastapi import status

def test_create_customer(client, test_token):
    headers = {"Authorization": f"Bearer {test_token}"}
    customer_data = {
        "name": "New Customer",
        "email": "newcustomer@example.com",
        "phone_number": "9876543210",
        "business_type": "commercial"
    }
    response = client.post("/api/customers/", headers=headers, json=customer_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == customer_data["name"]
    assert data["email"] == customer_data["email"]
    assert data["business_type"] == customer_data["business_type"]

def test_create_customer_unauthorized(client):
    customer_data = {
        "name": "New Customer",
        "email": "newcustomer@example.com",
        "phone_number": "9876543210",
        "business_type": "commercial"
    }
    response = client.post("/api/customers/", json=customer_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_create_customer_duplicate_email(client, test_token, test_customer):
    headers = {"Authorization": f"Bearer {test_token}"}
    customer_data = {
        "name": "Duplicate Customer",
        "email": test_customer.email,
        "phone_number": "9876543210",
        "business_type": "commercial"
    }
    response = client.post("/api/customers/", headers=headers, json=customer_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Email already registered" in response.json()["detail"]

def test_get_customers(client, test_token):
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get("/api/customers/", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "name" in data[0]
    assert "email" in data[0]

def test_get_customer_by_id(client, test_token, test_customer):
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get(f"/api/customers/{test_customer.id}", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == test_customer.name
    assert data["email"] == test_customer.email

def test_get_nonexistent_customer(client, test_token):
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get("/api/customers/999", headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_customer(client, test_token, test_customer):
    headers = {"Authorization": f"Bearer {test_token}"}
    update_data = {
        "name": "Updated Customer",
        "phone_number": "9876543210",
        "business_type": "residential"
    }
    response = client.put(
        f"/api/customers/{test_customer.id}",
        headers=headers,
        json=update_data
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["phone_number"] == update_data["phone_number"]
    assert data["business_type"] == update_data["business_type"]

def test_update_customer_unauthorized(client, test_customer):
    update_data = {
        "name": "Updated Customer",
        "phone_number": "9876543210",
        "business_type": "residential"
    }
    response = client.put(
        f"/api/customers/{test_customer.id}",
        json=update_data
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_delete_customer(client, test_token, test_customer):
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.delete(f"/api/customers/{test_customer.id}", headers=headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verify customer is deleted
    response = client.get(f"/api/customers/{test_customer.id}", headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_customer_unauthorized(client, test_customer):
    response = client.delete(f"/api/customers/{test_customer.id}")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_create_location(client, test_token, test_customer):
    headers = {"Authorization": f"Bearer {test_token}"}
    location_data = {
        "name": "New Location",
        "address": "456 New St",
        "city": "New City",
        "state": "NS",
        "zip_code": "54321",
        "country": "New Country"
    }
    response = client.post(
        f"/api/customers/{test_customer.id}/locations",
        headers=headers,
        json=location_data
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == location_data["name"]
    assert data["address"] == location_data["address"]
    assert data["customer_id"] == test_customer.id

def test_create_location_unauthorized(client, test_customer):
    location_data = {
        "name": "New Location",
        "address": "456 New St",
        "city": "New City",
        "state": "NS",
        "zip_code": "54321",
        "country": "New Country"
    }
    response = client.post(
        f"/api/customers/{test_customer.id}/locations",
        json=location_data
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_customer_locations(client, test_token, test_customer, test_location):
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get(
        f"/api/customers/{test_customer.id}/locations",
        headers=headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["name"] == test_location.name
    assert data[0]["customer_id"] == test_customer.id

def test_get_location(client, test_token, test_customer, test_location):
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get(
        f"/api/customers/{test_customer.id}/locations/{test_location.id}",
        headers=headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == test_location.name
    assert data["customer_id"] == test_customer.id

def test_get_nonexistent_location(client, test_token, test_customer):
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get(
        f"/api/customers/{test_customer.id}/locations/999",
        headers=headers
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_location(client, test_token, test_customer, test_location):
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.delete(
        f"/api/customers/{test_customer.id}/locations/{test_location.id}",
        headers=headers
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verify location is deleted
    response = client.get(
        f"/api/customers/{test_customer.id}/locations/{test_location.id}",
        headers=headers
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_location_unauthorized(client, test_customer, test_location):
    response = client.delete(
        f"/api/customers/{test_customer.id}/locations/{test_location.id}"
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED 