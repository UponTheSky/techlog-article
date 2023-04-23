from abc import ABC, abstractmethod

from pydantic import BaseModel, Field

from common.utils.jwt import JWTToken


class LoginDTO(BaseModel):
    username: str = Field(description="username following the OAuth2 specification")
    password: str = Field(description="password following the OAuth2 specification")


class LoginPort(ABC):
    @abstractmethod
    async def login(self, *, login_dto: LoginDTO) -> JWTToken:
        ...
