from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, Enum, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base

class AuditType(str, enum.Enum):
    VISUAL = "visual"
    HYDROSTATIC = "hydrostatic"
    ULTRASONIC = "ultrasonic"
    MAINTENANCE = "maintenance"
    CERTIFICATION = "certification"
    INVENTORY = "inventory"

class AuditStatus(str, enum.Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class AuditResult(str, enum.Enum):
    PASS = "pass"
    FAIL = "fail"
    CONDITIONAL = "conditional"
    PENDING = "pending"

class AuditRecord(Base):
    __tablename__ = "audit_records"

    id = Column(Integer, primary_key=True, index=True)
    cylinder_id = Column(Integer, ForeignKey("cylinders.id"), nullable=False)
    inspector_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    
    # Audit details
    audit_type = Column(Enum(AuditType), nullable=False)
    status = Column(Enum(AuditStatus), default=AuditStatus.SCHEDULED)
    result = Column(Enum(AuditResult), default=AuditResult.PENDING)
    scheduled_date = Column(DateTime(timezone=True), nullable=False)
    completed_date = Column(DateTime(timezone=True))
    
    # Inspection criteria
    visual_inspection = Column(JSON)  # Checklist of visual inspection points
    pressure_test = Column(JSON)  # Pressure test results and readings
    wall_thickness = Column(Float)  # For ultrasonic testing
    valve_condition = Column(String(200))
    thread_condition = Column(String(200))
    external_condition = Column(String(200))
    internal_condition = Column(String(200))
    
    # Certification
    certification_number = Column(String(100))
    certification_date = Column(DateTime(timezone=True))
    certification_expiry = Column(DateTime(timezone=True))
    certifying_authority = Column(String(200))
    
    # Results and recommendations
    defects_found = Column(String(500))
    recommendations = Column(String(500))
    maintenance_required = Column(Boolean, default=False)
    maintenance_details = Column(String(500))
    next_inspection_date = Column(DateTime(timezone=True))
    
    # Documentation
    report_number = Column(String(100))
    documents = Column(JSON)  # URLs or references to inspection documents
    photos = Column(JSON)  # URLs or references to inspection photos
    
    # Tracking
    notes = Column(String(1000))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("users.id"))
    last_modified_by = Column(Integer, ForeignKey("users.id"))

    # Relationships
    cylinder = relationship("Cylinder", back_populates="audit_records")
    inspector = relationship("User", foreign_keys=[inspector_id], backref="inspections")
    location = relationship("Location", back_populates="audit_records")
    creator = relationship("User", foreign_keys=[created_by], backref="created_audits")
    modifier = relationship("User", foreign_keys=[last_modified_by], backref="modified_audits")

    def __repr__(self):
        return f"<AuditRecord {self.id} - Cylinder {self.cylinder_id} - Type {self.audit_type}>" 