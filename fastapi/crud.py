from sqlalchemy.orm import Session
from models import DetectionData
from schemas import DetectionDataSchema

def create_detection_data(db: Session, detection_data: DetectionDataSchema):
    db_detection = DetectionData(**detection_data.dict())  # Convert Pydantic model to dict
    db.add(db_detection)
    db.commit()
    db.refresh(db_detection)
    return db_detection

def get_detection_data(db: Session):
    return db.query(DetectionData).all()
