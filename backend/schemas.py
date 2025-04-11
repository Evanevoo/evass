from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from models.user import UserRole
from models.cylinder import CylinderStatus, CylinderType
from models.movement import MovementType, TransactionStatus
from models.maintenance import MaintenanceType, MaintenanceStatus

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: UserRole
    phone_number: str
    address: str

class UserCreate(UserBase):
    password: str
    license_number: Optional[str] = None
    vehicle_id: Optional[str] = None
    certification: Optional[str] = None

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    license_number: Optional[str] = None
    vehicle_id: Optional[str] = None
    certification: Optional[str] = None

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True

# Cylinder schemas
class CylinderBase(BaseModel):
    serial_number: str
    type: CylinderType
    capacity: float
    pressure_rating: float
    tare_weight: float

class CylinderCreate(CylinderBase):
    pass

class CylinderUpdate(BaseModel):
    status: Optional[CylinderStatus] = None
    last_inspection: Optional[datetime] = None
    next_inspection: Optional[datetime] = None

class Cylinder(CylinderBase):
    id: int
    barcode: str
    qr_code: str
    status: CylinderStatus
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Customer schemas
class LocationBase(BaseModel):
    name: str
    address: str
    city: str
    state: str
    zip_code: str
    country: str
    is_primary: bool = False

class LocationCreate(LocationBase):
    customer_id: int

class Location(LocationBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class CustomerBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    address: str
    city: str
    state: str
    zip_code: str
    country: str
    business_type: str
    tax_id: str
    credit_limit: float
    payment_terms: str

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None
    business_type: Optional[str] = None
    tax_id: Optional[str] = None
    credit_limit: Optional[float] = None
    payment_terms: Optional[str] = None

class Customer(CustomerBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    locations: List[Location] = []

    class Config:
        from_attributes = True

# Movement schemas
class CylinderMovementBase(BaseModel):
    cylinder_id: int
    movement_type: MovementType
    from_location_id: int
    to_location_id: int
    notes: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class CylinderMovementCreate(CylinderMovementBase):
    pass

class CylinderMovement(CylinderMovementBase):
    id: int
    performed_by: int
    timestamp: datetime

    class Config:
        from_attributes = True

# Transaction schemas
class TransactionItemBase(BaseModel):
    cylinder_id: int
    quantity: int
    unit_price: float

class TransactionItemCreate(TransactionItemBase):
    pass

class TransactionItem(TransactionItemBase):
    id: int
    transaction_id: int
    total_price: float

    class Config:
        from_attributes = True

class TransactionBase(BaseModel):
    customer_id: int
    transaction_type: MovementType
    notes: Optional[str] = None

class TransactionCreate(TransactionBase):
    items: List[TransactionItemCreate]

class Transaction(TransactionBase):
    id: int
    status: TransactionStatus
    total_amount: float
    created_at: datetime
    completed_at: Optional[datetime] = None
    items: List[TransactionItem] = []

    class Config:
        from_attributes = True

# Maintenance schemas
class MaintenanceRecordBase(BaseModel):
    cylinder_id: int
    maintenance_type: MaintenanceType
    scheduled_date: datetime
    notes: Optional[str] = None
    cost: Optional[float] = None

class MaintenanceRecordCreate(MaintenanceRecordBase):
    pass

class MaintenanceRecordUpdate(BaseModel):
    status: Optional[MaintenanceStatus] = None
    completed_date: Optional[datetime] = None
    pressure_test_result: Optional[float] = None
    visual_inspection_result: Optional[bool] = None
    leak_test_result: Optional[bool] = None
    notes: Optional[str] = None
    cost: Optional[float] = None

class MaintenanceRecord(MaintenanceRecordBase):
    id: int
    status: MaintenanceStatus
    performed_by: int
    completed_date: Optional[datetime] = None
    pressure_test_result: Optional[float] = None
    visual_inspection_result: Optional[bool] = None
    leak_test_result: Optional[bool] = None

    class Config:
        from_attributes = True

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None 