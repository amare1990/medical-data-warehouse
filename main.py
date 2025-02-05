"""
Exposing data using fast api
"""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class DetectionDataSchema(BaseModel):
  class_name: str
  confidence: float
  bbox: dict
