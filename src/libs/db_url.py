import os
from config import config

def make_url():
    db_user = config.settings.db_user
    password = config.settings.password
    host = config.settings.host
    port = config.settings.port
    db = config.settings.db

    url = f"postgres://{db_user}:{password}@{host}:{port}/{db}"
    return url
