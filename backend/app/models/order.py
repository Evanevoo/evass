from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, Enum, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base

class OrderType(str, enum.Enum):
    DELIVERY = "delivery"
    PICKUP = "pickup"
    EXCHANGE = "exchange"
    TRANSFER = "transfer"
    RETURN = "return"

class OrderStatus(str, enum.Enum):
    DRAFT = "draft"
    PENDING = "pending"
    CONFIRMED = "confirmed"
    ASSIGNED = "assigned"
    IN_TRANSIT = "in_transit"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"

class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    PARTIALLY_PAID = "partially_paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(50), unique=True, index=True, nullable=False)
    order_type = Column(Enum(OrderType), nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.DRAFT)
    payment_status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    delivery_location_id = Column(Integer, ForeignKey("locations.id"))
    pickup_location_id = Column(Integer, ForeignKey("locations.id"))
    driver_id = Column(Integer, ForeignKey("users.id"))
    route_id = Column(Integer, ForeignKey("delivery_routes.id"))
    scheduled_date = Column(DateTime(timezone=True))
    delivery_date = Column(DateTime(timezone=True))
    order_total = Column(Float, default=0.0)
    tax_amount = Column(Float, default=0.0)
    discount_amount = Column(Float, default=0.0)
    final_amount = Column(Float, default=0.0)
    payment_terms = Column(String(255))
    special_instructions = Column(String(1000))
    customer_reference = Column(String(100))  # Customer's PO number
    signature = Column(String(1000))  # Base64 encoded signature
    proof_of_delivery = Column(String(1000))  # URL to POD document
    notes = Column(String(1000))
    metadata = Column(JSON)  # Additional order-specific data
    created_by = Column(Integer, ForeignKey("users.id"))
    last_modified_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    customer = relationship("Customer", back_populates="orders")
    delivery_location = relationship("Location", foreign_keys=[delivery_location_id])
    pickup_location = relationship("Location", foreign_keys=[pickup_location_id])
    driver = relationship("User", foreign_keys=[driver_id])
    route = relationship("DeliveryRoute", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")
    movements = relationship("CylinderMovement", back_populates="order")
    invoices = relationship("Invoice", back_populates="order")

    def __repr__(self):
        return f"<Order {self.order_number}>"

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    cylinder_id = Column(Integer, ForeignKey("cylinders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float)
    total_price = Column(Float)
    notes = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    order = relationship("Order", back_populates="order_items")
    cylinder = relationship("Cylinder")
    product = relationship("Product") 