from typing import List, Optional

from pydantic import BaseModel

"""
Schemas for Request body of different requests like create, delete, update, get.
FastAPI allows us to specify schemas in router functions which acts as data validator.
No need for a custom validator.
"""

# City base class
class CityBase(BaseModel):
    name: str
    area: int
    population: int
    roads: int
    trees: int

"""
Explanation :
This schema is for the Create API of city. It inherits the base class for City. 
Here all fields are mandatory. Our schema and FastAPI will make sure that happens
"""
class CityCreate(CityBase):
    pass

"""
Explanation: This schema is for the get API of city. Here we will be also returing id and country_name 
along with other data(since its inheriting base class) as we now know which country this city belongs to.
"""
class City(CityBase):
    id: int
    country_name: str

    class Config:
        orm_mode = True


"""
Explanation: This schema for Update API for City. Here all the fields are optional.
"""
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


