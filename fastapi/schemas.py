from pydantic import BaseModel

class DetectionDataSchema(BaseModel):
    class_name: str
    confidence: float
    bbox: dict

    class Config:
        orm_mode = True  # Allows Pydantic to work with SQLAlchemy models
