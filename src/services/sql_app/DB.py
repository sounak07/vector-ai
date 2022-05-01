from typing import List
from sqlalchemy.orm import Session
from . import User


class SqlDb():
    _db_conn: Session = None

    def __init__(self, db_conn: Session):
        SqlDb._db_conn = db_conn

    @classmethod
    def get_db_instance(cls):
        return cls._db_conn
