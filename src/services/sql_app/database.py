from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from libs.db_url import make_url


SQLALCHEMY_DATABASE_URL = make_url()

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo_pool=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
