from typing import Union
from abc import ABC, abstractmethod

from pydantic import BaseModel, Field

from common.utils.message import ServiceMessage
from common.utils.jwt import JWTToken


class LoginDTO(BaseModel):
    username: str = Field(description="username following the OAuth2 specification")
    password: str = Field(description="password following the OAuth2 specification")


class LoginPort(ABC):
    @abstractmethod
    def login(self, *, login_dto: LoginDTO) -> ServiceMessage[Union[JWTToken, str]]:
        ...
