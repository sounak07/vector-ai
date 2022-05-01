import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, JSON, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base

class ContinentModel(Base):
    __tablename__ = "continents" 

    id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR, index=True, unique=True)
    area = Column(Integer, default=0)
    population = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    countries = relationship("CountryModel", back_populates="continent", cascade="all, delete", passive_deletes=True)

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

    continent = relationship("ContinentModel", back_populates="countries")

    