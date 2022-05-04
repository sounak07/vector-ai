from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from common.error import InvalidInput, NotFound
from services.sql_app import crud, schemas
from services.sql_app.database import SessionLocal
from libs.response import response_out
from api.v1.schemas.response import SuccessResponse
from services.celery.celery_worker import create_continent_task, update_continent_task, delete_continent_task

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create", response_model=SuccessResponse)
def create_continent(continent: schemas.ContinentCreate, db: Session = Depends(get_db)):
    # we can use try catch to catch the error?
    db_user = crud.get_continent_by_name(db, name=continent.name)
    if db_user:
        raise InvalidInput(f"Oops! Continent {continent.name} already registered. There goes a rainbow...")
    # calling task queue
    res = create_continent_task.apply_async(args=["continent_create_task",continent.__dict__])
    return response_out("Continent register request received successfully", status.HTTP_200_OK, results={ "message_id": str(res)})


@router.get("", response_model=List[schemas.Continent])
def get_continents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    continents = crud.get_continents(db, skip=skip, limit=limit)
    return continents


@router.patch("/{continent_name}", response_model=SuccessResponse)
def update_continent_by_name(continent_name: str, continent: schemas.ContinentUpdate, db: Session = Depends(get_db)):
    continent_db = crud.get_continent_by_name(db, name=continent_name)
    if continent_db is None:
        raise NotFound(f"Oops! Continent {continent_name} not found. There goes a rainbow...")
    # for key, value in continent:
    res = update_continent_task.apply_async(["update_continent_task", continent_name ,continent.__dict__])
    return response_out("Continent update request received successfully", status.HTTP_200_OK, results={"message_id": str(res)})

@router.delete("/{continent_name}", response_model=SuccessResponse)
def delete_continent_by_name(continent_name: str, db: Session = Depends(get_db)):

    continent = crud.get_continent_by_name(db, name=continent_name)
    if continent is None:
        raise NotFound(f"Oops! Continent {continent_name} not found. There goes a rainbow...")

    res = delete_continent_task.apply_async(["delete_continent_task", continent_name])
    return response_out("Continent delete request received successfully", status.HTTP_200_OK, results={"message_id": str(res)})
