from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from libs.db_url import make_url

"""
make db connection
"""

SQLALCHEMY_DATABASE_URL = make_url()

"""
create the db engine to be used throughout the app
"""
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo_pool=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

"""
It will act as the base class for db models
"""
Base = declarative_base()
