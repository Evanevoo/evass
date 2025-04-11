from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Float, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base
import enum

class MaintenanceType(str, enum.Enum):
    INSPECTION = "inspection"
    HYDROSTATIC_TEST = "hydrostatic_test"
    REPAIR = "repair"
    REPLACEMENT = "replacement"
    CLEANING = "cleaning"

class MaintenanceStatus(str, enum.Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"

class MaintenanceRecord(Base):
    __tablename__ = "maintenance_records"

    id = Column(Integer, primary_key=True, index=True)
    cylinder_id = Column(Integer, ForeignKey("cylinders.id"))
    maintenance_type = Column(Enum(MaintenanceType))
    status = Column(Enum(MaintenanceStatus), default=MaintenanceStatus.SCHEDULED)
    scheduled_date = Column(DateTime(timezone=True))
    completed_date = Column(DateTime(timezone=True))
    performed_by = Column(Integer, ForeignKey("users.id"))
    notes = Column(String)
    cost = Column(Float)
    
    # Test results
    pressure_test_result = Column(Float, nullable=True)
    visual_inspection_result = Column(Boolean, nullable=True)
    leak_test_result = Column(Boolean, nullable=True)
    
    # Relationships
    cylinder = relationship("Cylinder", back_populates="maintenance_records")
    technician = relationship("User")
    
    def __repr__(self):
        return f"<MaintenanceRecord {self.id}>"

class MaintenanceSchedule(Base):
    __tablename__ = "maintenance_schedules"

    id = Column(Integer, primary_key=True, index=True)
    cylinder_id = Column(Integer, ForeignKey("cylinders.id"))
    maintenance_type = Column(Enum(MaintenanceType))
    frequency_days = Column(Integer)  # Days between maintenance
    last_maintenance = Column(DateTime(timezone=True))
    next_maintenance = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    cylinder = relationship("Cylinder")
    
    def __repr__(self):
        return f"<MaintenanceSchedule {self.id}>" 