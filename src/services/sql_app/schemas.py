from typing import List, Optional

from datetime import datetime
from pydantic import BaseModel


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

    class Config:
        orm_mode = True

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


