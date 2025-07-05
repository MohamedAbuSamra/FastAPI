from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models.country import Country
from app.schemas.product import CountryRead
from typing import List

router = APIRouter(prefix="/countries", tags=["countries"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[CountryRead], summary="List Countries")
def list_countries(db: Session = Depends(get_db)):
    return db.query(Country).all() 