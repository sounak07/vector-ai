from itertools import count
from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from common.error import InvalidInput, NotFound
from services.sql_app import crud, schemas
from services.sql_app.database import SessionLocal
from libs.response import response_out
from api.v1.schemas.response import SuccessResponse
from libs.utils import contains

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("", response_model=SuccessResponse)
def get_countries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    countries: List[schemas.Country] = crud.get_countries(db, skip=skip, limit=limit)
    return response_out("success", status.HTTP_200_OK, results={"countries": countries})

@router.post("/{continent_name}", response_model=SuccessResponse)
def create_country_by_continent(
    continent_name: str, country: schemas.CountryCreate, db: Session = Depends(get_db)):

    continent_info = crud.get_continent_by_name(db, name=continent_name)
    if continent_info is None:
        raise NotFound(f"Oops! Continent {continent_name} not found. There goes a rainbow...")

    countries_by_continent = crud.get_countries_by_continent(db, name=continent_name)
    continent_country_list = []
    total_population = 0
    total_area = 0
    for coun in countries_by_continent:
        obj = {
            "country": coun.name,
        }
        total_population += coun.population
        total_area += coun.area
        continent_country_list.append(obj)

    if contains(continent_country_list, lambda x: x["country"] == country.name):
        raise InvalidInput(f"Oops! Country {country.name} already registered. There goes a rainbow...")

    if(total_population + country.population > continent_info.population):
        raise InvalidInput(f"Oops! Total continent capacity exceeded. We can't accomodate any more people is {continent_name}!")

    if(total_area + country.area > continent_info.area):
        raise InvalidInput("Oops! Total continent area exceeded. We can't form any more countries!")

    new_country = crud.create_country(db=db, country=country, continent_name=continent_name)
    return response_out("Country registered successfully", status.HTTP_200_OK, results={"res": new_country})



