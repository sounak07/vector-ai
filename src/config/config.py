# config file to read ENVs which can be accessed through the app,handy feature from FastApi
import os
from pydantic import BaseSettings

from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    db_user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    db = os.getenv("DB_NAME")
    broker = os.getenv("CELERY_BROKER_URL")


settings = Settings()
