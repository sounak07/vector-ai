from sqlalchemy.orm import Session

from . import ContinentModel, CountryModel , schemas

def get_continents(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ContinentModel).offset(skip).limit(limit).all()

def get_continent_by_name(db: Session , name: str):
    return db.query(ContinentModel).filter(ContinentModel.name == name).first()

def create_continent(db: Session , continent: schemas.ContinentCreate):
    db_user = ContinentModel(**continent.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_countries(db: Session, skip: int = 0, limit: int = 100):
    return db.query(CountryModel).offset(skip).limit(limit).all()

def get_country_by_name(db: Session , name: str):
    return db.query(CountryModel).filter(CountryModel.name == name).first()

def create_country(db: Session , country: schemas.CountryCreate, continent_id: int):
    db_user = CountryModel(**country.dict(), continent_id=continent_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
