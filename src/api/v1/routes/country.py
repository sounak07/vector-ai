from itertools import count
from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from common.error import InvalidInput, NotFound
from services.sql_app import crud, schemas
from services.sql_app.database import SessionLocal
from libs.response import response_out
from api.v1.schemas.response import SuccessResponse

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/{continent_name}", response_model=SuccessResponse)
def create_country_by_continent(
    continent_name: str, country: schemas.CountryCreate, db: Session = Depends(get_db)):
    db_user = crud.get_continent_by_name(db, name=continent_name)
    if db_user is None:
        raise NotFound(f"Oops! Continent {continent_name} not found. There goes a rainbow...")
    db_user = crud.get_country_by_name(db, name=country.name)
    if db_user:
        raise InvalidInput(f"Oops! Country {country.name} already registered. There goes a rainbow...")
    new_country = crud.create_country(db=db, country=country, continent_name=continent_name)
    return response_out("Country registered successfully", status.HTTP_200_OK, results={"res": new_country})


@router.get("", response_model=SuccessResponse)
def get_countries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    countries: List[schemas.Country] = crud.get_countries(db, skip=skip, limit=limit)
    return response_out("success", status.HTTP_200_OK, results={"countries": countries})
