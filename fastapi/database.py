from sqlalchemy import create_engine, Column, String, Float, Integer, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Use PostgreSQL instead of SQLite
DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@" \
               f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

# Set up SQLAlchemy engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class DetectionData(Base):
    __tablename__ = "detection_data"

    id = Column(Integer, primary_key=True, index=True)
    class_name = Column(String, index=True)
    confidence = Column(Float)
    bbox = Column(JSON)

def init_db():
    """Create tables in the PostgreSQL database if they don't exist"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Provide a database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
