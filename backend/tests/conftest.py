import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from datetime import datetime, timedelta

from main import app
from database import Base, get_db
from auth import get_password_hash, create_access_token
from models.user import User
from models.cylinder import Cylinder
from models.customer import Customer, Location
from models.movement import CylinderMovement, Transaction, TransactionItem
from models.maintenance import MaintenanceRecord, MaintenanceSchedule

# Test database URL
TEST_DATABASE_URL = "sqlite:///:memory:"

# Create test engine and session
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session")
def test_db():
    # Create all tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop all tables
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session(test_db):
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture(scope="function")
def test_user(db_session):
    user = User(
        email="test@example.com",
        hashed_password=get_password_hash("testpassword"),
        full_name="Test User",
        role="admin",
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture(scope="function")
def test_token(test_user):
    return create_access_token({"sub": test_user.email})

@pytest.fixture(scope="function")
def test_customer(db_session):
    customer = Customer(
        name="Test Customer",
        email="customer@example.com",
        phone_number="1234567890",
        business_type="commercial"
    )
    db_session.add(customer)
    db_session.commit()
    db_session.refresh(customer)
    return customer

@pytest.fixture(scope="function")
def test_location(db_session, test_customer):
    location = Location(
        name="Test Location",
        address="123 Test St",
        city="Test City",
        state="TS",
        zip_code="12345",
        country="Test Country",
        customer_id=test_customer.id
    )
    db_session.add(location)
    db_session.commit()
    db_session.refresh(location)
    return location

@pytest.fixture(scope="function")
def test_cylinder(db_session):
    cylinder = Cylinder(
        serial_number="TEST123",
        type="Oxygen",
        capacity=50,
        pressure_rating=2000,
        tare_weight=30,
        status="available"
    )
    db_session.add(cylinder)
    db_session.commit()
    db_session.refresh(cylinder)
    return cylinder

@pytest.fixture(scope="function")
def test_maintenance_record(db_session, test_cylinder):
    record = MaintenanceRecord(
        cylinder_id=test_cylinder.id,
        maintenance_type="inspection",
        scheduled_date=datetime.now() + timedelta(days=30),
        status="scheduled",
        notes="Test maintenance"
    )
    db_session.add(record)
    db_session.commit()
    db_session.refresh(record)
    return record

@pytest.fixture(scope="function")
def test_transaction(db_session, test_customer, test_cylinder):
    transaction = Transaction(
        customer_id=test_customer.id,
        transaction_type="sale",
        status="pending",
        total_amount=100.00
    )
    db_session.add(transaction)
    db_session.commit()
    db_session.refresh(transaction)

    item = TransactionItem(
        transaction_id=transaction.id,
        cylinder_id=test_cylinder.id,
        quantity=1,
        unit_price=100.00
    )
    db_session.add(item)
    db_session.commit()
    db_session.refresh(transaction)
    return transaction

@pytest.fixture(scope="function")
def test_cylinder_movement(db_session, test_cylinder, test_location):
    movement = CylinderMovement(
        cylinder_id=test_cylinder.id,
        from_location_id=None,
        to_location_id=test_location.id,
        movement_type="delivery",
        notes="Test delivery"
    )
    db_session.add(movement)
    db_session.commit()
    db_session.refresh(movement)
    return movement

@pytest.fixture(scope="function")
def test_maintenance_schedule(db_session, test_cylinder):
    schedule = MaintenanceSchedule(
        cylinder_id=test_cylinder.id,
        maintenance_type="inspection",
        frequency_days=365,
        notes="Annual inspection"
    )
    db_session.add(schedule)
    db_session.commit()
    db_session.refresh(schedule)
    return schedule 