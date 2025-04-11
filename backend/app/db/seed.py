from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from app.core.auth import get_password_hash
import logging

logger = logging.getLogger(__name__)

def seed_admin_user(db: Session):
    admin_email = "admin@example.com"
    admin_password = "Admin@123!"  # This is just for initial setup, should be changed immediately
    
    try:
        # Check if admin user already exists
        existing_admin = db.query(User).filter(User.email == admin_email).first()
        if existing_admin:
            logger.info("Admin user already exists")
            return
        
        # Create admin user
        admin_user = User(
            email=admin_email,
            full_name="System Administrator",
            hashed_password=get_password_hash(admin_password),
            role=UserRole.ADMIN.value,  # Ensure the value is correct (string/integer)
            is_active=True
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        logger.info("Admin user created successfully")
        logger.warning("IMPORTANT: Change the admin password immediately after first login!")
    except Exception as e:
        logger.error(f"Error occurred while creating admin user: {str(e)}")
        db.rollback()  # Rollback in case of error
