import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, JSON, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base

"""
To decleare the db models and its relation ships between different models

Relationships for our app : 
ContinentModel <-> CountryModel <-> CityModel [ <-> represents bidirectional relationships ]

"""

class ContinentModel(Base):
    __tablename__ = "continents" 

    id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR, index=True, unique=True)
    area = Column(Integer, default=0)
    population = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    """
    cascade="all, delete", passive_deletes=True is added to ensure if parent is deleted child also gets deleted. 
    Read more: https://docs.sqlalchemy.org/en/14/orm/cascades.html#passive-deletes
    
    """
    countries = relationship("CountryModel", back_populates="continent" ,cascade="all, delete", passive_deletes=True)

class CountryModel(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR, index=True, unique=True)
    continent_name = Column(String, ForeignKey("continents.name", ondelete="CASCADE"))
    area = Column(Integer, default=0)
    hospitals = Column(Integer, default=0)
    parks = Column(Integer, default=0)
    population = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    """
    country has relationship with both city and continent.
    """
    continent = relationship("ContinentModel", back_populates="countries")
    cities = relationship("CityModel", cascade="all, delete", passive_deletes=True)

class CityModel(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR, index=True, unique=True)
    country_name = Column(String, ForeignKey("countries.name", ondelete="CASCADE"))
    area = Column(Integer, default=0)
    roads = Column(Integer, default=0)
    trees = Column(Integer, default=0)
    population = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    country = relationship("CountryModel", back_populates="cities")
    
