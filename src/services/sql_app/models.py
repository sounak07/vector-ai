import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, JSON, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base


class ContinentModel(Base):
    __tablename__ = "continents" 
    __table_args__ = {"schema": "vector_world"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    area = Column(Integer, default=0)
    population = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    countries = relationship("CountryModel", back_populates="countinent")

class CountryModel(Base):
    __tablename__ = "countries"
    __table_args__ = {"schema": "vector_world"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    continent_id = Column(Integer, ForeignKey("continents.id"))
    area = Column(Integer, default=0)
    hospitals = Column(Integer, default=0)
    parks = Column(Integer, default=0)
    population = Column(Integer, default=0)
    # created_at = Column(DateTime, default=datetime.datetime.utcnow)
    # updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


    countinent = relationship("CountryModel", back_populates="countries")