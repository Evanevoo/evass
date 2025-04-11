from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, Enum, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base

class MaintenanceType(str, enum.Enum):
    INSPECTION = "inspection"
    HYDRO_TEST = "hydro_test"
    REPAIR = "repair"
    CLEANING = "cleaning"
    PAINTING = "painting"
    VALVE_REPLACEMENT = "valve_replacement"
    RECERTIFICATION = "recertification"
    OTHER = "other"

class MaintenanceStatus(str, enum.Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class MaintenanceOutcome(str, enum.Enum):
    PASS = "pass"
    FAIL = "fail"
    NEEDS_REPAIR = "needs_repair"
    NEEDS_REPLACEMENT = "needs_replacement"
    RETIRED = "retired"

class MaintenanceRecord(Base):
    __tablename__ = "maintenance_records"

    id = Column(Integer, primary_key=True, index=True)
    cylinder_id = Column(Integer, ForeignKey("cylinders.id"), nullable=False)
    maintenance_type = Column(Enum(MaintenanceType), nullable=False)
    status = Column(Enum(MaintenanceStatus), default=MaintenanceStatus.SCHEDULED)
    outcome = Column(Enum(MaintenanceOutcome))
    location_id = Column(Integer, ForeignKey("locations.id"))
    technician_id = Column(Integer, ForeignKey("users.id"))
    scheduled_date = Column(DateTime(timezone=True))
    start_date = Column(DateTime(timezone=True))
    completion_date = Column(DateTime(timezone=True))
    next_maintenance_date = Column(DateTime(timezone=True))
    cost = Column(Float)
    work_order_number = Column(String(50))
    description = Column(String(1000))
    findings = Column(String(1000))
    recommendations = Column(String(1000))
    parts_used = Column(JSON)  # List of parts and quantities
    test_results = Column(JSON)  # Test measurements and results
    attachments = Column(JSON)  # URLs to related documents/images
    certification_number = Column(String(100))
    notes = Column(String(1000))
    created_by = Column(Integer, ForeignKey("users.id"))
    last_modified_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    cylinder = relationship("Cylinder", back_populates="maintenance_records")
    location = relationship("Location")
    technician = relationship("User", foreign_keys=[technician_id])
    creator = relationship("User", foreign_keys=[created_by])
    modifier = relationship("User", foreign_keys=[last_modified_by])

    def __repr__(self):
        return f"<MaintenanceRecord {self.id} - {self.maintenance_type}>" 