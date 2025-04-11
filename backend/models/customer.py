from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    zip_code = Column(String)
    country = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Business details
    business_type = Column(String)
    tax_id = Column(String)
    credit_limit = Column(Float)
    payment_terms = Column(String)
    
    # Relationships
    locations = relationship("Location", back_populates="customer")
    cylinders = relationship("Cylinder", back_populates="customer")
    transactions = relationship("Transaction", back_populates="customer")
    
    def __repr__(self):
        return f"<Customer {self.name}>"

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    name = Column(String)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    zip_code = Column(String)
    country = Column(String)
    is_primary = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    customer = relationship("Customer", back_populates="locations")
    cylinders = relationship("Cylinder", back_populates="location")
    
    def __repr__(self):
        return f"<Location {self.name}>" 