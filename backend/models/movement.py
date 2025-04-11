from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base
import enum

class MovementType(str, enum.Enum):
    DELIVERY = "delivery"
    PICKUP = "pickup"
    TRANSFER = "transfer"
    MAINTENANCE = "maintenance"
    RETURN = "return"

class TransactionStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"

class CylinderMovement(Base):
    __tablename__ = "cylinder_movements"

    id = Column(Integer, primary_key=True, index=True)
    cylinder_id = Column(Integer, ForeignKey("cylinders.id"))
    movement_type = Column(Enum(MovementType))
    from_location_id = Column(Integer, ForeignKey("locations.id"))
    to_location_id = Column(Integer, ForeignKey("locations.id"))
    performed_by = Column(Integer, ForeignKey("users.id"))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    notes = Column(String)
    
    # Geolocation data
    latitude = Column(Float)
    longitude = Column(Float)
    
    # Relationships
    cylinder = relationship("Cylinder", back_populates="movements")
    from_location = relationship("Location", foreign_keys=[from_location_id])
    to_location = relationship("Location", foreign_keys=[to_location_id])
    user = relationship("User")
    
    def __repr__(self):
        return f"<CylinderMovement {self.id}>"

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    transaction_type = Column(Enum(MovementType))
    status = Column(Enum(TransactionStatus), default=TransactionStatus.PENDING)
    total_amount = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    notes = Column(String)
    
    # Relationships
    customer = relationship("Customer", back_populates="transactions")
    items = relationship("TransactionItem", back_populates="transaction")
    
    def __repr__(self):
        return f"<Transaction {self.id}>"

class TransactionItem(Base):
    __tablename__ = "transaction_items"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"))
    cylinder_id = Column(Integer, ForeignKey("cylinders.id"))
    quantity = Column(Integer)
    unit_price = Column(Float)
    total_price = Column(Float)
    
    # Relationships
    transaction = relationship("Transaction", back_populates="items")
    cylinder = relationship("Cylinder")
    
    def __repr__(self):
        return f"<TransactionItem {self.id}>" 