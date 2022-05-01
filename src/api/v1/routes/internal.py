from itertools import count
from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from common.error import InvalidInput
from services.sql_app import crud, schemas
from services.sql_app.database import SessionLocal
from api.v1.schemas.response import SuccessResponse
from libs.response import response_out
from api.v1.schemas.response import SuccessResponseResults

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/continent", response_model=SuccessResponseResults)
def create_continent(continent: schemas.ContinentCreate, db: Session = Depends(get_db)):
    db_user = crud.get_continent_by_name(db, name=continent.name)
    if db_user:
        raise InvalidInput(f"Oops! Continent {continent.name} already registered. There goes a rainbow...")
    crud.create_continent(db=db, continent=continent)
    return response_out("Continent registered successfully", status.HTTP_200_OK, results={"data": db_user})


@router.get("/continents", response_model=SuccessResponseResults)
def get_continents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    continents = crud.get_continents(db, skip=skip, limit=limit)
    return response_out("success", status.HTTP_200_OK, results={"continents": continents})


@router.get("/continents/{continent_name}", response_model=SuccessResponse)
def get_continent_by_name(continent_name: int, db: Session = Depends(get_db)):
    db_user = crud.get_continent_by_name(db, user_id=continent_name)
    if db_user is None:
        InvalidInput(f"Oops! Continent {continent_name} not found. There goes a rainbow...")
    return db_user


@router.post("/continents/{continent_name}/country", response_model=SuccessResponse)
def create_country_by_continent(
    continent_name: str, country: schemas.CountryCreate, db: Session = Depends(get_db)):
    db_user = crud.get_continent_by_name(db, name=continent_name)
    if db_user is None:
        raise InvalidInput(f"Oops! Continent {continent_name} not found. There goes a rainbow...")
    db_user = crud.get_country_by_name(db, name=country.name)
    if db_user:
        raise InvalidInput(f"Oops! Country {country.name} already registered. There goes a rainbow...")
    db_user = crud.create_country(db=db, country=country, continent_name=continent_name)
    return response_out("Country registered successfully", status.HTTP_200_OK)


@router.get("/countries/", response_model=SuccessResponseResults)
def get_countries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    countries: List[schemas.Country] = crud.get_countries(db, skip=skip, limit=limit)
    return response_out("success", status.HTTP_200_OK, results={"countries": countries})