from app.db.base import Base
from app.db.session import engine

def create_tables() -> None:
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_tables()
    print("Tables created successfully!") 