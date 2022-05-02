from typing import List

from fastapi import APIRouter, Depends, status
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

@router.get("", response_model=List[schemas.Country])
def get_countries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    countries: List[schemas.Country] = crud.get_countries(db, skip=skip, limit=limit)
    return countries

@router.post("/{continent_name}", response_model=SuccessResponse)
def create_country_by_continent(
    continent_name: str, country: schemas.CountryCreate, db: Session = Depends(get_db)):

    continent_info = crud.get_continent_by_name(db, name=continent_name)
    if continent_info is None:
        raise NotFound(f"Oops! Continent {continent_name} not found. There goes a rainbow...")

    country_info = crud.get_country_by_name(db, country.name)
    if country_info:
        raise InvalidInput(f"Oops! Country {country.name} already registered. There goes a rainbow...")

    countries_by_continent = crud.get_countries_by_continent(db, name=continent_name)
    total_population = 0
    total_area = 0
    for instance in countries_by_continent:
        total_population += instance.population
        total_area += instance.area

    if(total_population + country.population > continent_info.population):
        raise InvalidInput(f"Oops! Total continent capacity exceeded. We can't accomodate any more people in {continent_name}!")

    if(total_area + country.area > continent_info.area):
        raise InvalidInput("Oops! Total continent area exceeded. We can't form any more countries!")

    new_country = crud.create_country(db=db, country=country, continent_name=continent_name)
    return response_out("Country registered successfully", status.HTTP_200_OK, results={"res": new_country})



