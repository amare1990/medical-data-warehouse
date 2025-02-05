from sqlalchemy.orm import Session
from models import DetectionData
from schemas import DetectionDataSchema

def create_detection_data(db: Session, detection_data: DetectionDataSchema):
    db_detection = DetectionData(
        id=detection_data.id,
        class_name=detection_data.class_name,
        confidence=detection_data.confidence,
        bbox=detection_data.bbox.dict()  # If bbox is a dictionary, ensure it's correctly formatted
    )
    db.add(db_detection)
    db.commit()
    db.refresh(db_detection)
    return db_detection
