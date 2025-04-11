from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from typing import List, Dict
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64

from database import get_db
from models.cylinder import Cylinder, CylinderStatus
from models.movement import CylinderMovement, Transaction
from models.maintenance import MaintenanceRecord
from models.customer import Customer
from models.user import User
from auth import get_current_active_user

router = APIRouter()

@router.get("/dashboard")
async def get_dashboard_metrics(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Get total cylinders
    total_cylinders = db.query(func.count(Cylinder.id)).scalar()
    
    # Get cylinders by status
    cylinders_by_status = db.query(
        Cylinder.status,
        func.count(Cylinder.id)
    ).group_by(Cylinder.status).all()
    
    # Get total customers
    total_customers = db.query(func.count(Customer.id)).scalar()
    
    # Get recent transactions
    recent_transactions = db.query(Transaction).order_by(
        Transaction.created_at.desc()
    ).limit(5).all()
    
    # Get upcoming maintenance
    today = datetime.utcnow()
    upcoming_maintenance = db.query(MaintenanceRecord).filter(
        MaintenanceRecord.scheduled_date >= today,
        MaintenanceRecord.status == "scheduled"
    ).order_by(MaintenanceRecord.scheduled_date).limit(5).all()
    
    return {
        "total_cylinders": total_cylinders,
        "cylinders_by_status": dict(cylinders_by_status),
        "total_customers": total_customers,
        "recent_transactions": recent_transactions,
        "upcoming_maintenance": upcoming_maintenance
    }

@router.get("/cylinder-status")
async def get_cylinder_status_analytics(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Get cylinders by status
    status_counts = db.query(
        Cylinder.status,
        func.count(Cylinder.id)
    ).group_by(Cylinder.status).all()
    
    # Create pie chart
    plt.figure(figsize=(10, 6))
    plt.pie(
        [count for _, count in status_counts],
        labels=[status for status, _ in status_counts],
        autopct='%1.1f%%'
    )
    plt.title('Cylinder Status Distribution')
    
    # Save plot to bytes
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.getvalue()).decode()
    plt.close()
    
    return {
        "status_counts": dict(status_counts),
        "plot": plot_data
    }

@router.get("/movement-trends")
async def get_movement_trends(
    days: int = 30,  # Default to last 30 days
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Get movement counts by type for the specified period
    start_date = datetime.utcnow() - timedelta(days=days)
    
    movement_counts = db.query(
        CylinderMovement.movement_type,
        func.count(CylinderMovement.id)
    ).filter(
        CylinderMovement.timestamp >= start_date
    ).group_by(CylinderMovement.movement_type).all()
    
    # Create bar chart
    plt.figure(figsize=(12, 6))
    sns.barplot(
        x=[movement_type for movement_type, _ in movement_counts],
        y=[count for _, count in movement_counts]
    )
    plt.title(f'Cylinder Movements (Last {days} Days)')
    plt.xlabel('Movement Type')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    
    # Save plot to bytes
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.getvalue()).decode()
    plt.close()
    
    return {
        "movement_counts": dict(movement_counts),
        "plot": plot_data
    }

@router.get("/maintenance-analytics")
async def get_maintenance_analytics(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if current_user.role not in ["admin", "manager", "technician"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Get maintenance records by type
    maintenance_counts = db.query(
        MaintenanceRecord.maintenance_type,
        func.count(MaintenanceRecord.id)
    ).group_by(MaintenanceRecord.maintenance_type).all()
    
    # Get maintenance completion rate
    total_maintenance = db.query(func.count(MaintenanceRecord.id)).scalar()
    completed_maintenance = db.query(func.count(MaintenanceRecord.id)).filter(
        MaintenanceRecord.status == "completed"
    ).scalar()
    
    completion_rate = (completed_maintenance / total_maintenance * 100) if total_maintenance > 0 else 0
    
    # Get average time to complete maintenance
    avg_completion_time = db.query(
        func.avg(
            func.extract('epoch', MaintenanceRecord.completed_date - MaintenanceRecord.scheduled_date) / 86400
        )
    ).filter(
        MaintenanceRecord.status == "completed"
    ).scalar()
    
    return {
        "maintenance_counts": dict(maintenance_counts),
        "completion_rate": completion_rate,
        "avg_completion_time_days": avg_completion_time
    }

@router.get("/customer-analytics")
async def get_customer_analytics(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Get top customers by cylinder count
    top_customers = db.query(
        Customer.name,
        func.count(Cylinder.id)
    ).join(
        Cylinder,
        Customer.id == Cylinder.current_customer_id
    ).group_by(
        Customer.id
    ).order_by(
        func.count(Cylinder.id).desc()
    ).limit(10).all()
    
    # Get customer distribution by business type
    business_type_distribution = db.query(
        Customer.business_type,
        func.count(Customer.id)
    ).group_by(Customer.business_type).all()
    
    return {
        "top_customers": [{"name": name, "cylinder_count": count} for name, count in top_customers],
        "business_type_distribution": dict(business_type_distribution)
    }

@router.get("/export/report")
async def export_analytics_report(
    report_type: str,
    start_date: datetime = None,
    end_date: datetime = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    if not start_date:
        start_date = datetime.utcnow() - timedelta(days=30)
    if not end_date:
        end_date = datetime.utcnow()
    
    if report_type == "movements":
        # Get movement data
        movements = db.query(CylinderMovement).filter(
            CylinderMovement.timestamp.between(start_date, end_date)
        ).all()
        
        # Convert to DataFrame
        data = [{
            "timestamp": m.timestamp,
            "cylinder_id": m.cylinder_id,
            "movement_type": m.movement_type,
            "from_location": m.from_location_id,
            "to_location": m.to_location_id,
            "performed_by": m.performed_by
        } for m in movements]
        
        df = pd.DataFrame(data)
        
    elif report_type == "maintenance":
        # Get maintenance data
        maintenance = db.query(MaintenanceRecord).filter(
            MaintenanceRecord.scheduled_date.between(start_date, end_date)
        ).all()
        
        # Convert to DataFrame
        data = [{
            "scheduled_date": m.scheduled_date,
            "completed_date": m.completed_date,
            "cylinder_id": m.cylinder_id,
            "maintenance_type": m.maintenance_type,
            "status": m.status,
            "performed_by": m.performed_by
        } for m in maintenance]
        
        df = pd.DataFrame(data)
        
    elif report_type == "transactions":
        # Get transaction data
        transactions = db.query(Transaction).filter(
            Transaction.created_at.between(start_date, end_date)
        ).all()
        
        # Convert to DataFrame
        data = [{
            "created_at": t.created_at,
            "completed_at": t.completed_at,
            "customer_id": t.customer_id,
            "transaction_type": t.transaction_type,
            "status": t.status,
            "total_amount": t.total_amount
        } for t in transactions]
        
        df = pd.DataFrame(data)
        
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid report type"
        )
    
    # Convert DataFrame to CSV
    csv_data = df.to_csv(index=False)
    
    return {
        "report_type": report_type,
        "start_date": start_date,
        "end_date": end_date,
        "data": csv_data
    } 