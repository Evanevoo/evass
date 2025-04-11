from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base
import enum

class CylinderStatus(str, enum.Enum):
    AVAILABLE = "available"
    IN_USE = "in_use"
    MAINTENANCE = "maintenance"
    LOST = "lost"
    SCRAPPED = "scrapped"

class CylinderType(str, enum.Enum):
    OXYGEN = "oxygen"
    NITROGEN = "nitrogen"
    ARGON = "argon"
    CO2 = "co2"
    ACETYLENE = "acetylene"
    HELIUM = "helium"

class Cylinder(Base):
    __tablename__ = "cylinders"

    id = Column(Integer, primary_key=True, index=True)
    serial_number = Column(String, unique=True, index=True)
    barcode = Column(String, unique=True, index=True)
    qr_code = Column(String, unique=True, index=True)
    type = Column(Enum(CylinderType))
    capacity = Column(Float)  # in liters
    pressure_rating = Column(Float)  # in PSI
    tare_weight = Column(Float)  # in kg
    status = Column(Enum(CylinderStatus), default=CylinderStatus.AVAILABLE)
    last_inspection = Column(DateTime(timezone=True))
    next_inspection = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    current_location_id = Column(Integer, ForeignKey("locations.id"))
    current_customer_id = Column(Integer, ForeignKey("customers.id"))
    
    # Track history
    movements = relationship("CylinderMovement", back_populates="cylinder")
    maintenance_records = relationship("MaintenanceRecord", back_populates="cylinder")
    
    def __repr__(self):
        return f"<Cylinder {self.serial_number}>" 