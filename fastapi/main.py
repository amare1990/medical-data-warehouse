"""
Exposing data using fast api
"""

from fastapi import FastAPI
from pydantic import BaseModel
from database import Database
from crud import create_detection_data, get_detection_data

app = FastAPI()

class DetectionDataSchema(BaseModel):
  class_name: str
  confidence: float
  bbox: dict


@app.post("/add-detection/")
async def add_detection(data: DetectionDataSchema):
    try:
        create_detection_data(data.dict())
        return {"message": "Detection data added successfully!"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/get-detection/")
async def get_detections():
    try:
        detections = get_detection_data()
        return {"detections": detections}
    except Exception as e:
        return {"error": str(e)}
