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

@router.post("/create", response_model=SuccessResponse)
def create_continent(continent: schemas.ContinentCreate, db: Session = Depends(get_db)):
    db_user = crud.get_continent_by_name(db, name=continent.name)
    if db_user:
        raise InvalidInput(f"Oops! Continent {continent.name} already registered. There goes a rainbow...")
    continent = crud.create_continent(db=db, continent=continent)
    return response_out("Continent registered successfully", status.HTTP_200_OK, results={"res": continent})


@router.get("", response_model=List[schemas.Continent])
def get_continents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    continents = crud.get_continents(db, skip=skip, limit=limit)
    return continents


@router.get("/{continent_name}", response_model=schemas.Continent)
def get_continent_by_name(continent_name: str, db: Session = Depends(get_db)):
    continent = crud.get_continent_by_name(db, name=continent_name)
    if continent is None:
        raise NotFound(f"Oops! Continent {continent_name} not found. There goes a rainbow...")
    return continent

@router.patch("/{continent_name}", response_model=SuccessResponse)
def update_continent_by_name(continent_name: str, continent: schemas.ContinentUpdate, db: Session = Depends(get_db)):
    continent_db = crud.get_continent_by_name(db, name=continent_name)
    if continent_db is None:
        raise NotFound(f"Oops! Continent {continent_name} not found. There goes a rainbow...")
    updated_continent = crud.update_continent(db, continent=continent, continent_db=continent_db)
    return response_out("Continent updated successfully", status.HTTP_200_OK, results={"res": updated_continent})

@router.delete("/{continent_name}", response_model=SuccessResponse)
def delete_continent_by_name(continent_name: str, db: Session = Depends(get_db)):
    continent = crud.get_continent_by_name(db, name=continent_name)
    if continent is None:
        raise NotFound(f"Oops! Continent {continent_name} not found. There goes a rainbow...")
    res = crud.delete_continent(db, continent_db=continent)
    return response_out("Continent deleted successfully", status.HTTP_200_OK, results={"res": res})
