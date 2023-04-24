from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class CreateUserDTO:
    username: str
    hashed_password: str
    email: str


class CreateUserPort(ABC):
    @abstractmethod
    async def create_user(self, *, dto: CreateUserDTO) -> None:
        ...
