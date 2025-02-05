from sqlalchemy import Column, Integer, String, Float, JSON
from database import Base  # Make sure this now refers to PostgreSQL

class DetectionData(Base):
    __tablename__ = "detection_data"
    __table_args__ = {'extend_existing': True}  # Add this line

    id = Column(Integer, primary_key=True, index=True)
    class_name = Column(String, index=True)
    confidence = Column(Float)
    bbox = Column(JSON)  # JSON format works with PostgreSQL
