from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import qrcode
import os
from io import BytesIO
from fastapi.responses import StreamingResponse

from database import get_db
from models.cylinder import Cylinder
from models.user import User
from schemas import (
    CylinderCreate,
    Cylinder as CylinderSchema,
    CylinderUpdate
)
from auth import get_current_active_user

router = APIRouter()

@router.post("/", response_model=CylinderSchema)
async def create_cylinder(
    cylinder: CylinderCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Generate unique barcode and QR code
    # In a real system, you would use a proper barcode generation system
    barcode = f"GC{cylinder.serial_number.zfill(8)}"
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(barcode)
    qr.make(fit=True)
    qr_code = qr.make_image(fill_color="black", back_color="white")
    
    # Save QR code to bytes
    qr_bytes = BytesIO()
    qr_code.save(qr_bytes, format="PNG")
    qr_bytes.seek(0)
    
    # Create cylinder
    db_cylinder = Cylinder(
        serial_number=cylinder.serial_number,
        barcode=barcode,
        qr_code=barcode,  # Store barcode as QR code identifier
        type=cylinder.type,
        capacity=cylinder.capacity,
        pressure_rating=cylinder.pressure_rating,
        tare_weight=cylinder.tare_weight
    )
    
    db.add(db_cylinder)
    db.commit()
    db.refresh(db_cylinder)
    return db_cylinder

@router.get("/", response_model=List[CylinderSchema])
async def read_cylinders(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    cylinders = db.query(Cylinder).offset(skip).limit(limit).all()
    return cylinders

@router.get("/{cylinder_id}", response_model=CylinderSchema)
async def read_cylinder(
    cylinder_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    cylinder = db.query(Cylinder).filter(Cylinder.id == cylinder_id).first()
    if cylinder is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cylinder not found"
        )
    return cylinder

@router.put("/{cylinder_id}", response_model=CylinderSchema)
async def update_cylinder(
    cylinder_id: int,
    cylinder_update: CylinderUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    cylinder = db.query(Cylinder).filter(Cylinder.id == cylinder_id).first()
    if cylinder is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cylinder not found"
        )
    
    # Update cylinder fields
    for field, value in cylinder_update.dict(exclude_unset=True).items():
        setattr(cylinder, field, value)
    
    db.commit()
    db.refresh(cylinder)
    return cylinder

@router.delete("/{cylinder_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cylinder(
    cylinder_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    cylinder = db.query(Cylinder).filter(Cylinder.id == cylinder_id).first()
    if cylinder is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cylinder not found"
        )
    
    db.delete(cylinder)
    db.commit()
    return None

@router.get("/{cylinder_id}/qr-code")
async def get_cylinder_qr_code(
    cylinder_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    cylinder = db.query(Cylinder).filter(Cylinder.id == cylinder_id).first()
    if cylinder is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cylinder not found"
        )
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(cylinder.barcode)
    qr.make(fit=True)
    qr_code = qr.make_image(fill_color="black", back_color="white")
    
    # Save QR code to bytes
    qr_bytes = BytesIO()
    qr_code.save(qr_bytes, format="PNG")
    qr_bytes.seek(0)
    
    return StreamingResponse(qr_bytes, media_type="image/png")

@router.get("/search/{identifier}")
async def search_cylinder(
    identifier: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Search by serial number, barcode, or QR code
    cylinder = db.query(Cylinder).filter(
        (Cylinder.serial_number == identifier) |
        (Cylinder.barcode == identifier) |
        (Cylinder.qr_code == identifier)
    ).first()
    
    if cylinder is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cylinder not found"
        )
    
    return cylinder 