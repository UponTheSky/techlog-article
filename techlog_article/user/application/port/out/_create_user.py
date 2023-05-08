from abc import ABC, abstractmethod

from pydantic import BaseModel


class CreateUserDTO(BaseModel):
    username: str
    hashed_password: str
    email: str


class CreateUserAuthPort(ABC):
    @abstractmethod
    async def create_user_with_auth(self, *, dto: CreateUserDTO) -> None:
        ...
