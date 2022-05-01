import email
from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from services.sql_app import crud, models, schemas
from services.sql_app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/continent", response_model=schemas.Continent)
def create_continent(data: schemas.ContinentCreate, db: Session = Depends(get_db)):
    db_user = crud.get_continent_by_name(db, name=data.name)
    if db_user:
        raise HTTPException(status_code=400, detail="Continent already registered")
    return crud.create_continent(db=db, user=data)


@router.get("/continents", response_model=List[schemas.Continent])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    continents = crud.get_continents(db, skip=skip, limit=limit)
    return continents


@router.get("/continents/{continent_name}", response_model=schemas.Continent)
def read_user(continent_name: int, db: Session = Depends(get_db)):
    db_user = crud.get_continent_by_name(db, user_id=continent_name)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Continent not found")
    return db_user


@router.post("/continents/{continent_id}/country", response_model=schemas.Country)
def create_country_by_continent(
    continent_id: int, country: schemas.CountryCreate, db: Session = Depends(get_db)
):
    return crud.create_country(db=db, country=country, user_id=continent_id)


@router.get("/countries/", response_model=List[schemas.Country])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_countries(db, skip=skip, limit=limit)
    return items