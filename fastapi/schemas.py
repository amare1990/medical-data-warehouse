from pydantic import BaseModel

class BoundingBox(BaseModel):
    xmin: int
    xmax: int
    ymin: int
    ymax: int

class DetectionDataSchema(BaseModel):
    id: int
    class_name: str
    confidence: float
    bbox: BoundingBox

    class Config:
        from_attributes = True  # Instead of `orm_mode = True` in Pydantic V2

