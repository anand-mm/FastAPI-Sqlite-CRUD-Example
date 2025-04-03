from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

def create_table():
    print("Creating tables...") 
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")
    
def get_db():
    db = SessionLocal()  # Create a new session
    try:
        yield db  # Provide the session to the route
    finally:
        db.close()  # Ensure session cleanup