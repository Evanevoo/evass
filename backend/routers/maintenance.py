from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta

from database import get_db
from models.maintenance import MaintenanceRecord, MaintenanceSchedule
from models.cylinder import Cylinder
from models.user import User
from schemas import (
    MaintenanceRecordCreate,
    MaintenanceRecord as MaintenanceRecordSchema,
    MaintenanceRecordUpdate
)
from auth import get_current_active_user

router = APIRouter()

@router.post("/", response_model=MaintenanceRecordSchema)
async def create_maintenance_record(
    maintenance: MaintenanceRecordCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if current_user.role not in ["admin", "manager", "technician"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Check if cylinder exists
    cylinder = db.query(Cylinder).filter(Cylinder.id == maintenance.cylinder_id).first()
    if cylinder is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cylinder not found"
        )
    
    # Create maintenance record
    db_maintenance = MaintenanceRecord(
        **maintenance.dict(),
        performed_by=current_user.id
    )
    
    db.add(db_maintenance)
    db.commit()
    db.refresh(db_maintenance)
    return db_maintenance

@router.get("/", response_model=List[MaintenanceRecordSchema])
async def read_maintenance_records(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    records = db.query(MaintenanceRecord).offset(skip).limit(limit).all()
    return records

@router.get("/cylinder/{cylinder_id}", response_model=List[MaintenanceRecordSchema])
async def read_cylinder_maintenance_history(
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
    
    records = db.query(MaintenanceRecord).filter(
        MaintenanceRecord.cylinder_id == cylinder_id
    ).order_by(MaintenanceRecord.scheduled_date.desc()).all()
    
    return records

@router.put("/{record_id}", response_model=MaintenanceRecordSchema)
async def update_maintenance_record(
    record_id: int,
    maintenance_update: MaintenanceRecordUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if current_user.role not in ["admin", "manager", "technician"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    record = db.query(MaintenanceRecord).filter(MaintenanceRecord.id == record_id).first()
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Maintenance record not found"
        )
    
    # Update record fields
    for field, value in maintenance_update.dict(exclude_unset=True).items():
        setattr(record, field, value)
    
    # If maintenance is completed, update cylinder's last inspection date
    if maintenance_update.status == "completed" and not record.completed_date:
        record.completed_date = datetime.utcnow()
        
        # Update cylinder's last inspection date
        cylinder = db.query(Cylinder).filter(Cylinder.id == record.cylinder_id).first()
        if cylinder:
            cylinder.last_inspection = record.completed_date
            
            # Set next inspection date based on maintenance type
            if record.maintenance_type == "inspection":
                cylinder.next_inspection = record.completed_date + timedelta(days=365)  # Annual inspection
    
    db.commit()
    db.refresh(record)
    return record

@router.get("/upcoming", response_model=List[MaintenanceRecordSchema])
async def get_upcoming_maintenance(
    days: int = 30,  # Default to next 30 days
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    today = datetime.utcnow()
    end_date = today + timedelta(days=days)
    
    upcoming = db.query(MaintenanceRecord).filter(
        MaintenanceRecord.scheduled_date >= today,
        MaintenanceRecord.scheduled_date <= end_date,
        MaintenanceRecord.status == "scheduled"
    ).order_by(MaintenanceRecord.scheduled_date).all()
    
    return upcoming

@router.get("/overdue", response_model=List[MaintenanceRecordSchema])
async def get_overdue_maintenance(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    today = datetime.utcnow()
    
    overdue = db.query(MaintenanceRecord).filter(
        MaintenanceRecord.scheduled_date < today,
        MaintenanceRecord.status == "scheduled"
    ).order_by(MaintenanceRecord.scheduled_date).all()
    
    return overdue

@router.post("/schedule/{cylinder_id}")
async def create_maintenance_schedule(
    cylinder_id: int,
    maintenance_type: str,
    frequency_days: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Check if cylinder exists
    cylinder = db.query(Cylinder).filter(Cylinder.id == cylinder_id).first()
    if cylinder is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cylinder not found"
        )
    
    # Create maintenance schedule
    schedule = MaintenanceSchedule(
        cylinder_id=cylinder_id,
        maintenance_type=maintenance_type,
        frequency_days=frequency_days,
        last_maintenance=cylinder.last_inspection,
        next_maintenance=cylinder.last_inspection + timedelta(days=frequency_days) if cylinder.last_inspection else datetime.utcnow() + timedelta(days=frequency_days)
    )
    
    db.add(schedule)
    db.commit()
    db.refresh(schedule)
    return schedule 