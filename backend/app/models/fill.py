from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, Enum, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base

class FillStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"

class FillRecord(Base):
    __tablename__ = "fill_records"

    id = Column(Integer, primary_key=True, index=True)
    cylinder_id = Column(Integer, ForeignKey("cylinders.id"), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    operator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Fill details
    fill_date = Column(DateTime(timezone=True), nullable=False)
    status = Column(Enum(FillStatus), default=FillStatus.PENDING)
    initial_pressure = Column(Float)  # PSI or Bar
    final_pressure = Column(Float)  # PSI or Bar
    fill_amount = Column(Float)  # Amount filled in appropriate unit (kg, liters, etc.)
    gas_purity = Column(Float)  # Percentage
    batch_number = Column(String(100))  # For gas batch tracking
    cost = Column(Float)  # Cost of filling
    
    # Quality control
    pressure_test_passed = Column(Boolean)
    leak_test_passed = Column(Boolean)
    purity_test_passed = Column(Boolean)
    test_notes = Column(String(500))
    
    # Tracking
    work_order_number = Column(String(100))
    notes = Column(String(1000))
    created_by = Column(Integer, ForeignKey("users.id"))
    last_modified_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    cylinder = relationship("Cylinder", back_populates="fill_records")
    location = relationship("Location", back_populates="fill_records")
    operator = relationship("User", foreign_keys=[operator_id], back_populates="operated_fills")
    creator = relationship("User", foreign_keys=[created_by], backref="created_fills")
    modifier = relationship("User", foreign_keys=[last_modified_by], backref="modified_fills")

    def __repr__(self):
        return f"<FillRecord {self.id} - Cylinder {self.cylinder_id}>" 