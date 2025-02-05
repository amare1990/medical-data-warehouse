from pydantic import BaseModel

class DetectionDataSchema(BaseModel):
    class_name: str
    confidence: float
    bbox: dict
