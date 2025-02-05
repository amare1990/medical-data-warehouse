from sqlalchemy.orm import Session
from models import DetectionData
from schemas import DetectionDataSchema

def create_detection_data(db: Session, detection_data: dict):
    db_detection = DetectionData(**detection_data)
    db.add(db_detection)
    db.commit()
    db.refresh(db_detection)
    return db_detection

def get_detection_data(db: Session):
    return db.query(DetectionData).all()
