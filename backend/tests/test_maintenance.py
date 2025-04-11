import pytest
from fastapi import status
from datetime import datetime, timedelta

def test_create_maintenance_record(client, test_token, test_cylinder):
    headers = {"Authorization": f"Bearer {test_token}"}
    maintenance_data = {
        "cylinder_id": test_cylinder.id,
        "maintenance_type": "inspection",
        "scheduled_date": (datetime.now() + timedelta(days=30)).isoformat(),
        "notes": "Regular inspection"
    }
    response = client.post(
        "/api/maintenance/",
        headers=headers,
        json=maintenance_data
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["cylinder_id"] == test_cylinder.id
    assert data["maintenance_type"] == "inspection"
    assert data["status"] == "scheduled"

def test_create_maintenance_record_unauthorized(client, test_cylinder):
    maintenance_data = {
        "cylinder_id": test_cylinder.id,
        "maintenance_type": "inspection",
        "scheduled_date": (datetime.now() + timedelta(days=30)).isoformat(),
        "notes": "Regular inspection"
    }
    response = client.post(
        "/api/maintenance/",
        json=maintenance_data
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_create_maintenance_record_invalid_cylinder(client, test_token):
    headers = {"Authorization": f"Bearer {test_token}"}
    maintenance_data = {
        "cylinder_id": 999,
        "maintenance_type": "inspection",
        "scheduled_date": (datetime.now() + timedelta(days=30)).isoformat(),
        "notes": "Regular inspection"
    }
    response = client.post(
        "/api/maintenance/",
        headers=headers,
        json=maintenance_data
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_get_maintenance_records(client, test_token):
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get("/api/maintenance/", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "cylinder_id" in data[0]
    assert "maintenance_type" in data[0]
    assert "status" in data[0]

def test_get_cylinder_maintenance_history(client, test_token, test_cylinder):
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get(
        f"/api/maintenance/cylinder/{test_cylinder.id}",
        headers=headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["cylinder_id"] == test_cylinder.id

def test_update_maintenance_record(client, test_token, test_maintenance_record):
    headers = {"Authorization": f"Bearer {test_token}"}
    update_data = {
        "status": "completed",
        "completion_date": datetime.now().isoformat(),
        "notes": "Inspection completed successfully"
    }
    response = client.put(
        f"/api/maintenance/{test_maintenance_record.id}",
        headers=headers,
        json=update_data
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "completed"
    assert data["completion_date"] is not None
    assert data["notes"] == "Inspection completed successfully"

def test_update_maintenance_record_unauthorized(client, test_maintenance_record):
    update_data = {
        "status": "completed",
        "completion_date": datetime.now().isoformat(),
        "notes": "Inspection completed successfully"
    }
    response = client.put(
        f"/api/maintenance/{test_maintenance_record.id}",
        json=update_data
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_upcoming_maintenance(client, test_token):
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get("/api/maintenance/upcoming", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "scheduled_date" in data[0]
    assert "status" in data[0]

def test_get_overdue_maintenance(client, test_token):
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get("/api/maintenance/overdue", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert "scheduled_date" in data[0] if data else True

def test_create_maintenance_schedule(client, test_token, test_cylinder):
    headers = {"Authorization": f"Bearer {test_token}"}
    schedule_data = {
        "maintenance_type": "inspection",
        "frequency_days": 365,
        "notes": "Annual inspection"
    }
    response = client.post(
        f"/api/maintenance/schedule/{test_cylinder.id}",
        headers=headers,
        json=schedule_data
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["cylinder_id"] == test_cylinder.id
    assert data["maintenance_type"] == "inspection"
    assert data["frequency_days"] == 365

def test_create_maintenance_schedule_unauthorized(client, test_cylinder):
    schedule_data = {
        "maintenance_type": "inspection",
        "frequency_days": 365,
        "notes": "Annual inspection"
    }
    response = client.post(
        f"/api/maintenance/schedule/{test_cylinder.id}",
        json=schedule_data
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_create_maintenance_schedule_invalid_cylinder(client, test_token):
    headers = {"Authorization": f"Bearer {test_token}"}
    schedule_data = {
        "maintenance_type": "inspection",
        "frequency_days": 365,
        "notes": "Annual inspection"
    }
    response = client.post(
        "/api/maintenance/schedule/999",
        headers=headers,
        json=schedule_data
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND 