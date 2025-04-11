from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, Enum, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base

class CylinderStatus(str, enum.Enum):
    IN_SERVICE = "in_service"
    IN_TRANSIT = "in_transit"
    AT_CUSTOMER = "at_customer"
    EMPTY = "empty"
    FULL = "full"
    MAINTENANCE = "maintenance"
    RETIRED = "retired"
    LOST = "lost"

class CylinderType(str, enum.Enum):
    OXYGEN = "oxygen"
    NITROGEN = "nitrogen"
    HELIUM = "helium"
    ARGON = "argon"
    CO2 = "co2"
    ACETYLENE = "acetylene"
    PROPANE = "propane"
    CUSTOM = "custom"

class Cylinder(Base):
    __tablename__ = "cylinders"

    id = Column(Integer, primary_key=True, index=True)
    serial_number = Column(String(50), unique=True, index=True, nullable=False)
    barcode = Column(String(100), unique=True, index=True)
    type = Column(String(50), nullable=False)
    gas_type = Column(Enum(CylinderType), nullable=False)
    capacity = Column(Float, nullable=False)  # in liters or kg
    working_pressure = Column(Float)  # in PSI or Bar
    manufacture_date = Column(DateTime(timezone=True))
    last_inspection_date = Column(DateTime(timezone=True))
    next_inspection_date = Column(DateTime(timezone=True))
    last_fill_date = Column(DateTime(timezone=True))
    last_hydro_test_date = Column(DateTime(timezone=True))
    next_hydro_test_date = Column(DateTime(timezone=True))
    status = Column(Enum(CylinderStatus), default=CylinderStatus.EMPTY)
    current_location = Column(String(255))  # Can be coordinates or location name
    current_customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    owner_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    last_modified_by = Column(Integer, ForeignKey("users.id"))
    specifications = Column(JSON)  # For custom specifications
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    current_customer = relationship("Customer", foreign_keys=[current_customer_id], back_populates="current_cylinders")
    owner = relationship("Customer", foreign_keys=[owner_id], back_populates="owned_cylinders")
    movements = relationship("CylinderMovement", back_populates="cylinder")
    maintenance_records = relationship("MaintenanceRecord", back_populates="cylinder")
    fill_records = relationship("FillRecord", back_populates="cylinder")
    lease_records = relationship("LeaseRecord", back_populates="cylinder")
    audit_records = relationship("AuditRecord", back_populates="cylinder")

    def __repr__(self):
        return f"<Cylinder {self.serial_number}>" 