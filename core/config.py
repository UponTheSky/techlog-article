import os

from pydantic import BaseSettings

# references:
# config boilerplate: https://github.com/teamhide/fastapi-boilerplate/blob/master/core/config.py
# DB settings: https://docs.sqlalchemy.org/en/20/dialects/mysql.html#module-sqlalchemy.dialects.mysql.pymysql


class BaseConfig(BaseSettings):
    ENV: str
    DEBUG: bool = True
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    DATABASE_URL: str


class LocalConfig(BaseConfig):
    ENV = "local"
    DATABASE_URL = "mysql+pymysql://root:1Q2w3e4r!@localhost/techlog_articles"


def get_config() -> BaseConfig:
    env = os.getenv("ENV", "local")
    config_type = {"local": LocalConfig()}

    return config_type[env]


config = get_config()
