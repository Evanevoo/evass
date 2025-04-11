from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, Enum, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base

class LeaseStatus(str, enum.Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    TERMINATED = "terminated"
    PENDING = "pending"

class LeaseRecord(Base):
    __tablename__ = "lease_records"

    id = Column(Integer, primary_key=True, index=True)
    cylinder_id = Column(Integer, ForeignKey("cylinders.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    
    # Lease details
    lease_start = Column(DateTime(timezone=True), nullable=False)
    lease_end = Column(DateTime(timezone=True))
    status = Column(Enum(LeaseStatus), default=LeaseStatus.PENDING)
    lease_rate = Column(Float)  # Cost per day/month
    deposit_amount = Column(Float)
    deposit_paid = Column(Boolean, default=False)
    contract_number = Column(String(100))
    
    # Terms and conditions
    terms = Column(String(2000))
    special_conditions = Column(String(1000))
    
    # Return details
    actual_return_date = Column(DateTime(timezone=True))
    return_condition = Column(String(500))
    damage_notes = Column(String(500))
    additional_charges = Column(Float, default=0.0)
    
    # Tracking
    notes = Column(String(1000))
    created_by = Column(Integer, ForeignKey("users.id"))
    last_modified_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    cylinder = relationship("Cylinder", back_populates="lease_records")
    customer = relationship("Customer", back_populates="lease_records")
    location = relationship("Location", back_populates="lease_records")
    creator = relationship("User", foreign_keys=[created_by], backref="created_leases")
    modifier = relationship("User", foreign_keys=[last_modified_by], backref="modified_leases")

    def __repr__(self):
        return f"<LeaseRecord {self.id} - Cylinder {self.cylinder_id} - Customer {self.customer_id}>" 