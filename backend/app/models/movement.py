from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base

class MovementType(str, enum.Enum):
    DELIVERY = "delivery"
    PICKUP = "pickup"
    TRANSFER = "transfer"
    RETURN = "return"
    MAINTENANCE = "maintenance"
    FILL = "fill"
    SCRAP = "scrap"

class MovementStatus(str, enum.Enum):
    PENDING = "pending"
    IN_TRANSIT = "in_transit"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"

class CylinderMovement(Base):
    __tablename__ = "cylinder_movements"

    id = Column(Integer, primary_key=True, index=True)
    movement_type = Column(Enum(MovementType), nullable=False)
    status = Column(Enum(MovementStatus), default=MovementStatus.PENDING)
    cylinder_id = Column(Integer, ForeignKey("cylinders.id"), nullable=False)
    from_location_id = Column(Integer, ForeignKey("locations.id"))
    to_location_id = Column(Integer, ForeignKey("locations.id"))
    from_customer_id = Column(Integer, ForeignKey("customers.id"))
    to_customer_id = Column(Integer, ForeignKey("customers.id"))
    order_id = Column(Integer, ForeignKey("orders.id"))
    driver_id = Column(Integer, ForeignKey("users.id"))
    scheduled_date = Column(DateTime(timezone=True))
    actual_date = Column(DateTime(timezone=True))
    notes = Column(String(1000))
    signature = Column(String(1000))  # Base64 encoded signature
    proof_of_delivery = Column(String(1000))  # URL to POD document
    barcode_scan = Column(String(100))
    gps_location = Column(String(100))
    metadata = Column(JSON)  # Additional movement-specific data
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    cylinder = relationship("Cylinder", back_populates="movements")
    from_location = relationship("Location", foreign_keys=[from_location_id])
    to_location = relationship("Location", foreign_keys=[to_location_id])
    from_customer = relationship("Customer", foreign_keys=[from_customer_id])
    to_customer = relationship("Customer", foreign_keys=[to_customer_id])
    order = relationship("Order", back_populates="movements")
    driver = relationship("User", foreign_keys=[driver_id])
    creator = relationship("User", foreign_keys=[created_by])

    def __repr__(self):
        return f"<CylinderMovement {self.id} - {self.movement_type}>" 