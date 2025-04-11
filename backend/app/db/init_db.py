import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base, engine, get_db
from app.db.seed import seed_admin_user
from app.models.user import User  # Import all models here

def init_db():
    print("Creating database tables...")
    # Drop all tables first
    Base.metadata.drop_all(bind=engine)
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")
    
    print("\nSeeding admin user...")
    # Seed admin user
    db = next(get_db())
    try:
        seed_admin_user(db)
        print("Admin user created successfully!")
    except Exception as e:
        print(f"Error seeding admin user: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    init_db() 