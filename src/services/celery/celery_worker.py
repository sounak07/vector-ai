from services.sql_app import schemas
from celery import Celery
from celery.utils.log import get_task_logger
from sqlalchemy.orm import Session
from config import config

celery = Celery('tasks', broker=config.settings.broker)
from services.sql_app.database import SessionLocal

# Create logger - enable to display messages on task logger
celery_log = get_task_logger(__name__)

from services.sql_app.crud import create_continent, update_continent, delete_continent, create_country, update_country, delete_country, create_city, update_city, delete_city


## Continent tasks
@celery.task(bind=True)
def create_continent_task(self, task_name, continent):
    db: Session = SessionLocal()
    create_continent(db, continent)
    # Display Log
    celery_log.info(f"{task_name} complete!")
    db.close()
    return f"Hi, Your request for {task_name} has completed!"

@celery.task(bind=True)
def update_continent_task(self, task_name, continent_name, continent_data):
    db: Session = SessionLocal()
    update_continent(db, continent_data=continent_data, continent_name=continent_name)
    # Display Log
    celery_log.info(f"{task_name} complete!")
    db.close()
    return f"Hi, Your request for {task_name} has completed!"

@celery.task(bind=True)
def delete_continent_task(self, task_name, continent_name):
    db: Session = SessionLocal()
    delete_continent(db, continent_name=continent_name)
    # Display Log
    celery_log.info(f"{task_name} complete!")
    db.close()
    return f"Hi, Your request for {task_name} has completed!"


## Country tasks

@celery.task(bind=True)
def create_country_task(self, task_name, country, continent_name):
    db: Session = SessionLocal()
    create_country(db, country=country, continent_name=continent_name)
    # Display Log
    celery_log.info(f"{task_name} complete!")
    db.close()
    return f"Hi, Your request for {task_name} has completed!"


@celery.task(bind=True)
def update_country_task(self, task_name, country_name, country_data):
    db: Session = SessionLocal()
    update_country(db, country_data=country_data,country_name=country_name)
    # Display Log
    celery_log.info(f"{task_name} complete!")
    db.close()
    return f"Hi, Your request for {task_name} has completed!"


@celery.task(bind=True)
def delete_country_task(self, task_name, country_name):
    db: Session = SessionLocal()
    delete_country(db, country_name=country_name)
    # Display Log
    celery_log.info(f"{task_name} complete!")
    db.close()
    return f"Hi, Your request for {task_name} has completed!"


## City tasks

@celery.task(bind=True)
def create_city_task(self, task_name, city, country_name):
    db = SessionLocal()
    create_city(db, city=city, country_name=country_name)
    # Display Log
    celery_log.info(f"{task_name} complete!")
    db.close()
    return f"Hi, Your request for {task_name} has completed!"

@celery.task(bind=True)
def update_city_task(self, task_name, city_name, city):
    db: Session = SessionLocal()
    update_city(db, city_data=city, city_name=city_name)
    # Display Log
    celery_log.info(f"{task_name} complete!")
    db.close()
    return f"Hi, Your request for {task_name} has completed!"


@celery.task(bind=True)
def delete_city_task(self, task_name, city_name):
    db: Session = SessionLocal()
    delete_city(db, city_name=city_name)
    # Display Log
    celery_log.info(f"{task_name} complete!")
    db.close()
    return f"Hi, Your request for {task_name} has completed!"


