from typing import List
from sqlalchemy.orm import Session

from . import ContinentModel, CountryModel , schemas, CityModel

def get_continents(db: Session, skip: int = 0, limit: int = 100) -> List[schemas.Continent]:
    return db.query(ContinentModel).offset(skip).limit(limit).all()

def get_continent_by_name(db: Session , name: str) -> schemas.Continent:
    return db.query(ContinentModel).filter(ContinentModel.name == name).first()

def create_continent(db: Session , continent: schemas.ContinentCreate) -> schemas.Continent:
    db_user = ContinentModel(**continent.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_continent(db: Session , continent: schemas.ContinentUpdate, continent_db: schemas.Continent) -> schemas.Continent:
    continent_data = continent.dict(exclude_unset=True)
    for key, value in continent_data.items():
        setattr(continent_db, key, value)
    db.add(continent_db)
    db.commit()
    db.refresh(continent_db)
    return continent_db

def delete_continent(db: Session ,continent_db: schemas.Continent) -> dict:
    db.delete(continent_db)
    db.commit()
    return {"deleted": True}

def get_countries(db: Session, skip: int = 0, limit: int = 100) -> List[schemas.Country]:
    return db.query(CountryModel).offset(skip).limit(limit).all()

def get_countries_by_continent(db: Session, name: str) -> List[schemas.Country]:
    res = db.query(CountryModel).filter(CountryModel.continent_name == name).all()
    return res

def get_country_by_name(db: Session , name: str) -> schemas.Country:
    return db.query(CountryModel).filter(CountryModel.name == name).first()

def create_country(db: Session , country: schemas.CountryCreate, continent_name: str) -> schemas.Country:
    db_user = CountryModel(**country.dict(), continent_name=continent_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_country(db: Session , country: schemas.CountryUpdate, country_db: schemas.Country) -> schemas.Country:
    country_data = country.dict(exclude_unset=True)
    for key, value in country_data.items():
        setattr(country_db, key, value)
    db.add(country_db)
    db.commit()
    db.refresh(country_db)
    return country_db

def delete_country(db: Session ,country_db: schemas.Country) -> dict:
    db.delete(country_db)
    db.commit()
    return {"deleted": True}

def get_cities(db: Session, skip: int = 0, limit: int = 100) -> List[schemas.City]:
    return db.query(CityModel).offset(skip).limit(limit).all()

def get_city_by_name(db: Session , name: str) -> schemas.City:
    return db.query(CityModel).filter(CityModel.name == name).first()

def get_cities_by_country(db: Session, name: str) -> List[schemas.City]:
    res = db.query(CityModel).filter(CityModel.country_name == name).all()
    return res

def create_city(db: Session , city: schemas.CityCreate, country_name: str) -> schemas.City:
    db_user = CityModel(**city.dict(), country_name=country_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_city(db: Session , city: schemas.CityCreate, city_db: schemas.City) -> schemas.City:
    city_data = city.dict(exclude_unset=True)
    for key, value in city_data.items():
        setattr(city_db, key, value)
    db.add(city_db)
    db.commit()
    db.refresh(city_db)
    return city_db

def delete_city(db: Session ,city_db: schemas.City) -> dict:
    db.delete(city_db)
    db.commit()
    return {"deleted": True}