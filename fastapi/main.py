"""
Exposing data using fast api
"""

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List  # Add this

from database import get_db, init_db
import crud, schemas

# Initialize database tables (Run this once at startup)
init_db()

app = FastAPI()

@app.post("/detection_data/", response_model=schemas.DetectionDataSchema)
def create_data(detection_data: schemas.DetectionDataSchema, db: Session = Depends(get_db)):
    return crud.create_detection_data(db, detection_data)

# @app.get("/detection_data/", response_model=list[schemas.DetectionDataSchema])
@app.get("/detection_data/", response_model=List[schemas.DetectionDataSchema])  # Use List instead of list[]
def get_data(db: Session = Depends(get_db)):
    return crud.get_detection_data(db)

