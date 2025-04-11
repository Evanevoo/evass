from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base

class CustomerType(str, enum.Enum):
    BUSINESS = "business"
    INDIVIDUAL = "individual"
    DISTRIBUTOR = "distributor"
    MANUFACTURER = "manufacturer"

class CustomerStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING = "pending"

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    customer_type = Column(Enum(CustomerType), nullable=False)
    status = Column(Enum(CustomerStatus), default=CustomerStatus.ACTIVE)
    account_number = Column(String(50), unique=True, index=True)
    tax_id = Column(String(50))
    billing_address = Column(String(500))
    shipping_address = Column(String(500))
    contact_person = Column(String(255))
    email = Column(String(255))
    phone = Column(String(50))
    mobile = Column(String(50))
    credit_limit = Column(Integer)
    payment_terms = Column(String(255))
    notes = Column(String(1000))
    custom_fields = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("users.id"))
    last_modified_by = Column(Integer, ForeignKey("users.id"))

    # Relationships
    current_cylinders = relationship("Cylinder", foreign_keys="[Cylinder.current_customer_id]", back_populates="current_customer")
    owned_cylinders = relationship("Cylinder", foreign_keys="[Cylinder.owner_id]", back_populates="owner")
    orders = relationship("Order", back_populates="customer")
    contracts = relationship("Contract", back_populates="customer")
    locations = relationship("Location", back_populates="customer")
    contacts = relationship("Contact", back_populates="customer")
    pricing = relationship("CustomerPricing", back_populates="customer")
    audit_records = relationship("AuditRecord", back_populates="customer")

    def __repr__(self):
        return f"<Customer {self.name}>" 