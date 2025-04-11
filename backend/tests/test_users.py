import pytest
from fastapi import status
from schemas import UserCreate, UserUpdate

def test_register_user(client):
    user_data = {
        "email": "newuser@example.com",
        "password": "password123",
        "full_name": "New User",
        "role": "manager"
    }
    response = client.post("/api/users/register", json=user_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["full_name"] == user_data["full_name"]
    assert data["role"] == user_data["role"]
    assert "id" in data
    assert "hashed_password" not in data

def test_register_existing_user(client, test_user):
    user_data = {
        "email": test_user.email,
        "password": "password123",
        "full_name": "Test User",
        "role": "manager"
    }
    response = client.post("/api/users/register", json=user_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Email already registered" in response.json()["detail"]

def test_login_user(client, test_user):
    login_data = {
        "username": test_user.email,
        "password": "password"
    }
    response = client.post("/api/users/token", data=login_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials(client, test_user):
    login_data = {
        "username": test_user.email,
        "password": "wrongpassword"
    }
    response = client.post("/api/users/token", data=login_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Incorrect email or password" in response.json()["detail"]

def test_get_current_user(client, test_token):
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get("/api/users/me", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "hashed_password" not in data

def test_get_current_user_unauthorized(client):
    response = client.get("/api/users/me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_users(client, test_token):
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get("/api/users/", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "email" in data[0]
    assert "hashed_password" not in data[0]

def test_get_user_by_id(client, test_token, test_user):
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get(f"/api/users/{test_user.id}", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == test_user.email
    assert "hashed_password" not in data

def test_get_nonexistent_user(client, test_token):
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get("/api/users/999", headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_user(client, test_token, test_user):
    headers = {"Authorization": f"Bearer {test_token}"}
    update_data = {
        "full_name": "Updated Name",
        "phone_number": "9876543210"
    }
    response = client.put(
        f"/api/users/{test_user.id}",
        headers=headers,
        json=update_data
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["full_name"] == update_data["full_name"]
    assert data["phone_number"] == update_data["phone_number"]

def test_update_user_unauthorized(client, test_user):
    update_data = {
        "full_name": "Updated Name",
        "phone_number": "9876543210"
    }
    response = client.put(
        f"/api/users/{test_user.id}",
        json=update_data
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_delete_user(client, test_token, test_user):
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.delete(f"/api/users/{test_user.id}", headers=headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verify user is deleted
    response = client.get(f"/api/users/{test_user.id}", headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_user_unauthorized(client, test_user):
    response = client.delete(f"/api/users/{test_user.id}")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_delete_nonexistent_user(client, test_token):
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.delete("/api/users/999", headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND 