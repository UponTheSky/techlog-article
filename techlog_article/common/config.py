from typing import Union
import os

from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings):
    ENV: str
    DEBUG: bool
    APP_HOST: str
    APP_PORT: int
    DB_URL: str


class AuthBaseConfig(BaseSettings):
    JWT_ENCODE_ALGORITHM: str
    PASSWORD_HASH_ALGORITHM: str
    JWT_SECRET_KEY: str
    ACCESS_TOKEN_EXPRIRES_IN: int
    ADMIN_USERNAME: str


class LocalConfig(BaseConfig):
    ENV: str = "local"
    DEBUG: bool = True
    APP_HOST: str = "127.0.0.1"
    APP_PORT: int = 8000
    DB_URL: str = (
        "postgresql+asyncpg://db_admin:1Q2w3e4r!@localhost:5432/techlog_article"
    )


class AuthLocalConfig(BaseSettings):
    JWT_ENCODE_ALGORITHM: str = "HS256"
    PASSWORD_HASH_ALGORITHM: str = "sha256_crypt"
    JWT_SECRET_KEY: str = "test"
    ACCESS_TOKEN_EXPRIRES_IN: int = 3600
    ADMIN_USERNAME: str = "test"


class LocalDockerConfig(LocalConfig):
    ENV: str = "local_docker"
    APP_HOST: str = "0.0.0.0"


class AuthLocalDockerConfig(AuthLocalConfig):
    ...


def get_config() -> Union[BaseConfig, LocalConfig]:
    env = os.getenv("ENV", "local")
    config_type = {"local": LocalConfig(), "local_docker": LocalDockerConfig()}

    return config_type[env]


def get_auth_config() -> Union[AuthBaseConfig, AuthLocalConfig]:
    env = os.getenv("ENV", "local")
    config_type = {"local": AuthLocalConfig(), "local_docker": AuthLocalDockerConfig()}

    return config_type[env]


config = get_config()
auth_config = get_auth_config()
