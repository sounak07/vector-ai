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

@router.get("", response_model=List[schemas.City])
def get_cities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cities: List[schemas.City] = crud.get_cities(db, skip=skip, limit=limit)
    return cities

@router.post("/{country_name}", response_model=SuccessResponse)
def create_city_by_country(
    country_name: str, city: schemas.CityCreate, db: Session = Depends(get_db)):

    country_info = crud.get_country_by_name(db, name=country_name)
    if country_info is None:
        raise NotFound(f"Oops! Country {country_name} not found. There goes a rainbow...")

    city_info = crud.get_city_by_name(db, city.name)
    if city_info:
        raise InvalidInput(f"Oops! City {city.name} already registered. There goes a rainbow...")

    cities_by_country = crud.get_cities_by_country(db, name=country_name)
    total_population = 0
    total_area = 0
    for instance in cities_by_country:
        total_population += instance.population
        total_area += instance.area

    if(total_population + city.population > country_info.population):
        raise InvalidInput(f"Oops! Total Country capacity exceeded. We can't accomodate any more people in {country_name}!")

    if(total_area + city.area > country_info.area):
        raise InvalidInput("Oops! Total country area exceeded. We can't form any more cities!")

    new_city = crud.create_city(db=db, city=city, country_name=country_name)
    return response_out("Country registered successfully", status.HTTP_200_OK, results={"res": new_city})



