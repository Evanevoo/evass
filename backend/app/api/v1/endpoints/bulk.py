from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from typing import List
from sqlalchemy.orm import Session
from app.core.auth import get_current_active_user
from app.db.session import get_db
from app.schemas.user import UserSchema
from app.schemas.customer import CustomerCreate, CustomerSchema
from app.schemas.cylinder import CylinderCreate, CylinderSchema
from app.crud import customer as customer_crud
from app.crud import cylinder as cylinder_crud
import pandas as pd
import io

router = APIRouter()

@router.post("/customers", response_model=List[CustomerSchema])
async def bulk_upload_customers(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_active_user)
):
    try:
        # Read the uploaded file
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents))
        
        # Validate required columns
        required_columns = ['name', 'address', 'phone', 'email', 'customerId', 'barcode']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise HTTPException(
                status_code=400,
                detail=f"Missing required columns: {', '.join(missing_columns)}"
            )
        
        # Process and validate each row
        customers = []
        errors = []
        
        for index, row in df.iterrows():
            try:
                customer_data = CustomerCreate(
                    name=row['name'],
                    contact={
                        'address': row['address'],
                        'phone': row['phone'],
                        'email': row['email']
                    },
                    customerId=row['customerId'],
                    barcode=row['barcode']
                )
                customer = customer_crud.create(db, obj_in=customer_data)
                customers.append(customer)
            except Exception as e:
                errors.append(f"Row {index + 2}: {str(e)}")
        
        if errors:
            raise HTTPException(
                status_code=400,
                detail={"errors": errors, "successful_uploads": len(customers)}
            )
        
        return customers
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/cylinders", response_model=List[CylinderSchema])
async def bulk_upload_cylinders(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_active_user)
):
    try:
        # Read the uploaded file
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents))
        
        # Validate required columns
        required_columns = ['serialNumber', 'type', 'size', 'condition', 'maintenanceStatus', 'customerId', 'barcode']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise HTTPException(
                status_code=400,
                detail=f"Missing required columns: {', '.join(missing_columns)}"
            )
        
        # Process and validate each row
        cylinders = []
        errors = []
        
        for index, row in df.iterrows():
            try:
                cylinder_data = CylinderCreate(
                    serialNumber=row['serialNumber'],
                    type=row['type'],
                    size=row['size'],
                    condition=row['condition'],
                    maintenanceStatus=row['maintenanceStatus'],
                    customerId=row['customerId'],
                    barcode=row['barcode']
                )
                cylinder = cylinder_crud.create(db, obj_in=cylinder_data)
                cylinders.append(cylinder)
            except Exception as e:
                errors.append(f"Row {index + 2}: {str(e)}")
        
        if errors:
            raise HTTPException(
                status_code=400,
                detail={"errors": errors, "successful_uploads": len(cylinders)}
            )
        
        return cylinders
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 