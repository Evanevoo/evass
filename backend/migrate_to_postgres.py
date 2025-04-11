import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from models import Base  # Import your models
import json
from datetime import datetime

def migrate_data():
    # Load environment variables
    load_dotenv()
    
    # Source SQLite database
    sqlite_url = "sqlite:///./gas_tracker.db"
    sqlite_engine = create_engine(sqlite_url)
    SQLiteSession = sessionmaker(bind=sqlite_engine)
    
    # Destination PostgreSQL database
    postgres_url = os.getenv("DATABASE_URL")
    if not postgres_url:
        raise ValueError("DATABASE_URL environment variable is required")
    
    postgres_engine = create_engine(postgres_url)
    PostgresSession = sessionmaker(bind=postgres_engine)
    
    # Create tables in PostgreSQL
    Base.metadata.create_all(postgres_engine)
    
    # Get all tables
    tables = Base.metadata.tables.keys()
    
    # Migrate data
    with SQLiteSession() as sqlite_session, PostgresSession() as postgres_session:
        for table_name in tables:
            print(f"Migrating {table_name}...")
            
            # Get all records from SQLite
            table = Base.metadata.tables[table_name]
            records = sqlite_session.query(table).all()
            
            # Insert into PostgreSQL
            for record in records:
                # Convert record to dictionary
                record_dict = {c.name: getattr(record, c.name) for c in record.__table__.columns}
                
                # Handle datetime objects
                for key, value in record_dict.items():
                    if isinstance(value, datetime):
                        record_dict[key] = value.isoformat()
                
                # Create new record in PostgreSQL
                postgres_session.execute(
                    table.insert().values(**record_dict)
                )
            
            postgres_session.commit()
            print(f"Migrated {len(records)} records from {table_name}")

if __name__ == "__main__":
    migrate_data()
    print("Migration completed successfully!") 