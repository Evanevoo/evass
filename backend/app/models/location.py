from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, Enum, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base

class LocationType(str, enum.Enum):
    WAREHOUSE = "warehouse"
    CUSTOMER_SITE = "customer_site"
    FILLING_STATION = "filling_station"
    MAINTENANCE_FACILITY = "maintenance_facility"
    DISTRIBUTION_CENTER = "distribution_center"
    OTHER = "other"

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    location_type = Column(Enum(LocationType), nullable=False)
    address_line1 = Column(String(255), nullable=False)
    address_line2 = Column(String(255))
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    postal_code = Column(String(20), nullable=False)
    country = Column(String(100), nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    contact_name = Column(String(255))
    contact_phone = Column(String(50))
    contact_email = Column(String(255))
    operating_hours = Column(JSON)  # Store hours of operation for each day
    special_instructions = Column(String(1000))
    is_active = Column(Boolean, default=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"))
    last_modified_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    customer = relationship("Customer", back_populates="locations")
    cylinder_movements = relationship("CylinderMovement", back_populates="location")
    inventory = relationship("LocationInventory", back_populates="location")
    delivery_routes = relationship("DeliveryRoute", secondary="route_locations", back_populates="locations")
    audit_records = relationship("AuditRecord", back_populates="location")

    def __repr__(self):
        return f"<Location {self.name}>" 