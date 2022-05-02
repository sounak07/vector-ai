from typing import List, Optional

from datetime import datetime
from pydantic import BaseModel

class CityBase(BaseModel):
    name: str
    area: int
    population: int
    roads: int
    trees: int


class CityCreate(CityBase):
    pass


class City(CityBase):
    id: int
    country_name: str

    class Config:
        orm_mode = True

class CityUpdate(BaseModel):
    area: Optional[int] = None
    population: Optional[int] = None
    roads: Optional[int] = None
    trees: Optional[int] = None

class CountryBase(BaseModel):
    name: str
    area: int
    population: int
    hospitals: int
    parks: int


class CountryCreate(CountryBase):
    pass

class Country(CountryBase):
    id: int
    continent_name: str
    cities: List[City]

    class Config:
        orm_mode = True


class CountryUpdate(BaseModel):
    area: Optional[int] = None
    population: Optional[int] = None
    parks: Optional[int] = None
    hospitals: Optional[int] = None


class ContinentBase(BaseModel):
    name: str
    area: int
    population: int


class ContinentCreate(ContinentBase):
    pass

class Continent(ContinentBase):
    id: int
    countries: List[Country]

    class Config:
        orm_mode = True


class ContinentUpdate(BaseModel):
    area: Optional[int] = None
    population: Optional[int] = None


