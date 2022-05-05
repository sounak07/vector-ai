from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from common.error import InvalidInput, NotFound
from services.sql_app import crud, schemas
from services.sql_app.database import SessionLocal
from libs.response import response_out
from api.v1.schemas.response import SuccessResponse

from services.celery.celery_worker import create_country_task, update_country_task, delete_country_task

router = APIRouter()

# Dependency to get db Session
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
        raise NotFound(f"Oops! Country {continent_name} not found. There goes a rainbow...")

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

    res = create_country_task.apply_async(args=["country_create_task", country.__dict__, continent_name])
    return response_out("Country register request received successfully", status.HTTP_200_OK, results={"message_id": str(res)})


@router.patch("/{country_name}", response_model=SuccessResponse)
def update_country_by_name(country_name: str, country: schemas.CountryUpdate, db: Session = Depends(get_db)):
    country_db = crud.get_country_by_name(db, name=country_name)
    if country_db is None:
        raise NotFound(f"Oops! Country {country_name} not found. There goes a rainbow...")
    
    ## optimize more
    if country.population is not None or country.area is not None:
        countries_by_continent = crud.get_countries_by_continent(db, name=country_db.continent_name)

        continent_info = crud.get_continent_by_name(db, name=country_db.continent_name)
        total_population = 0
        total_area = 0
        for instance in countries_by_continent:
            if instance.name == country_name:
                continue
            total_population += instance.population
            total_area += instance.area

        if(country.population is not None and total_population + country.population > continent_info.population):
            raise InvalidInput(
                f"Oops! Total continent capacity exceeded. We can't accomodate any more people in {country_name}!")

        if(country.area is not None and total_area + country.area > continent_info.area):
            raise InvalidInput(
                f"Oops! Total continent area exceeded. We can't increase any more area for {country_name}!")

    res = update_country_task.apply_async(args=["country_update_task", country_name, country.__dict__])
    return response_out("Country update request received successfully", status.HTTP_200_OK, results={"message_id": str(res)})


@router.delete("/{country_name}", response_model=SuccessResponse)
def delete_country_by_name(country_name: str, db: Session = Depends(get_db)):
    country = crud.get_country_by_name(db, name=country_name)
    if country is None:
        raise NotFound(f"Oops! Country {country_name} not found. There goes a rainbow...")
    # res = crud.delete_country(db, country_db=country)
    res = delete_country_task.apply_async(args=["country_delete_task", country_name])
    return response_out("Country delete request received successfully", status.HTTP_200_OK, results={"message_id": str(res)})

