from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from database import get_db
from models.movement import CylinderMovement, Transaction, TransactionItem
from models.cylinder import Cylinder
from models.customer import Customer, Location
from models.user import User
from schemas import (
    CylinderMovementCreate,
    CylinderMovement as CylinderMovementSchema,
    TransactionCreate,
    Transaction as TransactionSchema,
    TransactionItem as TransactionItemSchema
)
from auth import get_current_active_user

router = APIRouter()

@router.post("/cylinder", response_model=CylinderMovementSchema)
async def create_cylinder_movement(
    movement: CylinderMovementCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if current_user.role not in ["admin", "manager", "driver"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Check if cylinder exists
    cylinder = db.query(Cylinder).filter(Cylinder.id == movement.cylinder_id).first()
    if cylinder is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cylinder not found"
        )
    
    # Check if locations exist
    from_location = db.query(Location).filter(Location.id == movement.from_location_id).first()
    to_location = db.query(Location).filter(Location.id == movement.to_location_id).first()
    
    if not from_location or not to_location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location not found"
        )
    
    # Create movement
    db_movement = CylinderMovement(
        **movement.dict(),
        performed_by=current_user.id
    )
    
    # Update cylinder's current location
    cylinder.current_location_id = movement.to_location_id
    
    db.add(db_movement)
    db.commit()
    db.refresh(db_movement)
    return db_movement

@router.get("/cylinder", response_model=List[CylinderMovementSchema])
async def read_cylinder_movements(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    movements = db.query(CylinderMovement).offset(skip).limit(limit).all()
    return movements

@router.get("/cylinder/{cylinder_id}", response_model=List[CylinderMovementSchema])
async def read_cylinder_movement_history(
    cylinder_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Check if cylinder exists
    cylinder = db.query(Cylinder).filter(Cylinder.id == cylinder_id).first()
    if cylinder is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cylinder not found"
        )
    
    movements = db.query(CylinderMovement).filter(
        CylinderMovement.cylinder_id == cylinder_id
    ).order_by(CylinderMovement.timestamp.desc()).all()
    
    return movements

# Transaction endpoints
@router.post("/transaction", response_model=TransactionSchema)
async def create_transaction(
    transaction: TransactionCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Check if customer exists
    customer = db.query(Customer).filter(Customer.id == transaction.customer_id).first()
    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    # Calculate total amount
    total_amount = 0
    transaction_items = []
    
    for item in transaction.items:
        # Check if cylinder exists
        cylinder = db.query(Cylinder).filter(Cylinder.id == item.cylinder_id).first()
        if cylinder is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cylinder {item.cylinder_id} not found"
            )
        
        item_total = item.quantity * item.unit_price
        total_amount += item_total
        
        transaction_items.append(TransactionItem(
            cylinder_id=item.cylinder_id,
            quantity=item.quantity,
            unit_price=item.unit_price,
            total_price=item_total
        ))
    
    # Create transaction
    db_transaction = Transaction(
        customer_id=transaction.customer_id,
        transaction_type=transaction.transaction_type,
        total_amount=total_amount,
        notes=transaction.notes
    )
    
    db.add(db_transaction)
    db.flush()  # Get the transaction ID
    
    # Add transaction items
    for item in transaction_items:
        item.transaction_id = db_transaction.id
        db.add(item)
    
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@router.get("/transaction", response_model=List[TransactionSchema])
async def read_transactions(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    transactions = db.query(Transaction).offset(skip).limit(limit).all()
    return transactions

@router.get("/transaction/{transaction_id}", response_model=TransactionSchema)
async def read_transaction(
    transaction_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if transaction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    return transaction

@router.put("/transaction/{transaction_id}/complete", response_model=TransactionSchema)
async def complete_transaction(
    transaction_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if transaction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    if transaction.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Transaction is not in pending status"
        )
    
    transaction.status = "completed"
    transaction.completed_at = datetime.utcnow()
    
    db.commit()
    db.refresh(transaction)
    return transaction 