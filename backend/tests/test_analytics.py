import pytest
from fastapi import status
from datetime import datetime, timedelta

def test_get_cylinder_metrics(client, test_token):
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get("/api/analytics/cylinders/metrics", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "total_cylinders" in data
    assert "active_cylinders" in data
    assert "in_maintenance" in data
    assert "out_of_service" in data

def test_get_cylinder_metrics_unauthorized(client):
    response = client.get("/api/analytics/cylinders/metrics")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_cylinder_trends(client, test_token):
    headers = {"Authorization": f"Bearer {test_token}"}
    params = {
        "start_date": (datetime.now() - timedelta(days=30)).isoformat(),
        "end_date": datetime.now().isoformat()
    }
    response = client.get(
        "/api/analytics/cylinders/trends",
        headers=headers,
        params=params
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "movements" in data
    assert "maintenance" in data
    assert "status_changes" in data

def test_get_customer_metrics(client, test_token):
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get("/api/analytics/customers/metrics", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "total_customers" in data
    assert "active_customers" in data
    assert "cylinders_per_customer" in data

def test_get_transaction_metrics(client, test_token):
    headers = {"Authorization": f"Bearer {test_token}"}
    params = {
        "start_date": (datetime.now() - timedelta(days=30)).isoformat(),
        "end_date": datetime.now().isoformat()
    }
    response = client.get(
        "/api/analytics/transactions/metrics",
        headers=headers,
        params=params
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "total_transactions" in data
    assert "total_revenue" in data
    assert "average_transaction_value" in data

def test_get_maintenance_metrics(client, test_token):
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get("/api/analytics/maintenance/metrics", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "total_maintenance" in data
    assert "completed_maintenance" in data
    assert "upcoming_maintenance" in data
    assert "overdue_maintenance" in data

def test_get_location_metrics(client, test_token):
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get("/api/analytics/locations/metrics", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "total_locations" in data
    assert "cylinders_per_location" in data
    assert "active_locations" in data

def test_get_cylinder_utilization(client, test_token):
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get("/api/analytics/cylinders/utilization", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "utilization_rate" in data
    assert "idle_cylinders" in data
    assert "in_use_cylinders" in data

def test_get_customer_activity(client, test_token):
    headers = {"Authorization": f"Bearer {test_token}"}
    params = {
        "start_date": (datetime.now() - timedelta(days=30)).isoformat(),
        "end_date": datetime.now().isoformat()
    }
    response = client.get(
        "/api/analytics/customers/activity",
        headers=headers,
        params=params
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "transactions" in data
    assert "cylinder_movements" in data
    assert "top_customers" in data

def test_get_maintenance_efficiency(client, test_token):
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get("/api/analytics/maintenance/efficiency", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "average_completion_time" in data
    assert "on_time_completion_rate" in data
    assert "maintenance_types" in data

def test_get_financial_metrics(client, test_token):
    headers = {"Authorization": f"Bearer {test_token}"}
    params = {
        "start_date": (datetime.now() - timedelta(days=30)).isoformat(),
        "end_date": datetime.now().isoformat()
    }
    response = client.get(
        "/api/analytics/financial/metrics",
        headers=headers,
        params=params
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "revenue" in data
    assert "expenses" in data
    assert "profit" in data
    assert "average_transaction_value" in data 