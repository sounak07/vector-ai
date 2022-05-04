from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from common.error import InvalidInput, NotFound
from services.sql_app import crud, schemas
from services.sql_app.database import SessionLocal
from libs.response import response_out
from api.v1.schemas.response import SuccessResponse

from services.celery.celery_worker import create_city_task, update_city_task, delete_city_task

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

    res = create_city_task.apply_async(args=["city_create_task", city.__dict__, country_name])
    return response_out("City register request received successfully", status.HTTP_200_OK, results={"message_id": str(res)})

@router.patch("/{city_name}", response_model=SuccessResponse)
def update_country_by_name(city_name: str, city: schemas.CityUpdate, db: Session = Depends(get_db)):
    city_db = crud.get_city_by_name(db, name=city_name)
    if city_db is None:
        raise NotFound(f"Oops! Country {city_name} not found. There goes a rainbow...")
    
    ## optimize more
    if city.population is not None or city.area is not None:
        print("Sounak")
        cities_by_country = crud.get_cities_by_country(db, name=city_db.country_name)

        country_info = crud.get_country_by_name(db, name=city_db.country_name)
        total_population = 0
        total_area = 0
        for instance in cities_by_country:
            if instance.name == city_name:
                continue
            total_population += instance.population
            total_area += instance.area

        if(city.population is not None and total_population + city.population > country_info.population):
            raise InvalidInput(f"Oops! Total continent capacity exceeded. We can't accomodate any more people in {city_name}!")

        if(city.area is not None and total_area + city.area > country_info.area):
            raise InvalidInput(f"Oops! Total continent area exceeded. We can't increase any more area for {city_name}!")

    res = update_city_task.apply_async(args=["city_update_task", city_name, city.__dict__])
    return response_out("City update request received successfully", status.HTTP_200_OK, results={"message_id": str(res)})


@router.delete("/{city_name}", response_model=SuccessResponse)
def delete_city_by_name(city_name: str, db: Session = Depends(get_db)):
    city = crud.get_city_by_name(db, name=city_name)
    if city is None:
        raise NotFound(f"Oops! Country {city_name} not found. There goes a rainbow...")
    
    # res = crud.delete_city(db, city_db=city)
    res = delete_city_task.apply_async(args=["city_delete_task", city_name])
    return response_out("Country delete request received successfully", status.HTTP_200_OK, results={"message_id": str(res)})
