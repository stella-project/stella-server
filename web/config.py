import os
import json

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "change-me"
    AUTOMATOR_GH_KEY = os.environ.get("AUTOMATOR_GH_KEY") or None
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class PostgresConfig(Config):
    DEBUG = False
    POSTGRES_USER = os.environ.get("POSTGRES_USER") or "postgres"
    POSTGRES_PW = os.environ.get("POSTGRES_PW") or "change-me"
    POSTGRES_URL = os.environ.get("POSTGRES_URL") or "db:5432"
    POSTGRES_DB = os.environ.get("POSTGRES_DB") or "postgres"
    SQLALCHEMY_DATABASE_URI = "postgresql://{user}:{pw}@{url}/{db}".format(
        user=POSTGRES_USER, pw=POSTGRES_PW, url=POSTGRES_URL, db=POSTGRES_DB
    )
    STELLA_APP_ADDRESS = json.loads(os.environ.get("STELLA_APP_ADDRESS") or "[]")


class TestConfig(Config):
    TESTING = True
    DEBUG = True

    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DEV_DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "data-dev.sqlite")


config = {"postgres": PostgresConfig, "test": TestConfig}
