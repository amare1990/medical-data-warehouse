from sqlalchemy import Column, Integer, String, Float, JSON
from database import Base

class DetectionData(Base):
    __tablename__ = "detection_data"

    id = Column(Integer, primary_key=True, index=True)
    class_name = Column(String, index=True)
    confidence = Column(Float)
    bbox = Column(JSON)
