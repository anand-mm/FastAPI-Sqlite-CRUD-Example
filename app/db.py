from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from app.config import settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

engine = create_async_engine(settings.DATABASE_URL, echo=True)  # Async Engine


SessionLocal = sessionmaker(bind=engine, class_=AsyncSession,autoflush=False)
Base = declarative_base()

async def get_db():
    try:
        async with SessionLocal() as session:
            yield session
    finally:
      session.close()

# def create_table():
#     print("Creating tables...") 
#     Base.metadata.create_all(bind=engine)
#     print("Tables created successfully!")