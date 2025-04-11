from sqlalchemy import Boolean, Column, Integer, String, Enum, DateTime
from sqlalchemy.sql import func
from database import Base
import enum

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    DRIVER = "driver"
    CUSTOMER = "customer"
    TECHNICIAN = "technician"
    MANAGER = "manager"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    role = Column(Enum(UserRole))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True))
    phone_number = Column(String)
    address = Column(String)
    
    # Additional fields for drivers and technicians
    license_number = Column(String, nullable=True)
    vehicle_id = Column(String, nullable=True)
    certification = Column(String, nullable=True)
    
    def __repr__(self):
        return f"<User {self.email}>" 