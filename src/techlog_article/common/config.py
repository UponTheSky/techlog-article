from typing import Union
import os

from pydantic import BaseSettings


class BaseConfig(BaseSettings):
    ENV: str
    DEBUG: bool
    APP_HOST: str
    APP_PORT: int
    DB_URL: str


class AuthConfig(BaseSettings):
    JWT_ENCODE_ALGORITHM: str
    PASSWORD_HASH_ALGORITHM: str
    JWT_SECRET_KEY: str
    ACCESS_TOKEN_EXPRIRES_IN: int
    ADMIN_USERNAME: str


class DevelopmentConfig(BaseConfig):
    ENV = "development"
    DEBUG = True
    APP_HOST = "0.0.0.0"
    APP_PORT = 8000
    DB_URL = "postgresql+asyncpg://db_admin:1Q2w3e4r!@localhost:5432/techlog_article"


def get_config() -> Union[BaseConfig, DevelopmentConfig]:
    env = os.getenv("ENV", "development")
    config_type = {"development": DevelopmentConfig()}

    return config_type[env]


def get_auth_config() -> AuthConfig:
    return AuthConfig()


config = get_config()
auth_config = get_auth_config()
