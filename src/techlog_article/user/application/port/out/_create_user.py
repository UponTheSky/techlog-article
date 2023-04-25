from abc import ABC, abstractmethod

from pydantic import BaseModel


class CreateUserDTO(BaseModel):
    username: str
    hashed_password: str
    email: str


class CreateUserPort(ABC):
    @abstractmethod
    async def create_user(self, *, dto: CreateUserDTO) -> None:
        ...
