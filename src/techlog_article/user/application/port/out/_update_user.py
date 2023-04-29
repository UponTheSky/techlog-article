from typing import Optional
from abc import ABC, abstractmethod
from uuid import UUID

from pydantic import BaseModel

from ....domain import User


class UpdateUserDTO(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    hashed_password: Optional[str] = None


class UpdateUserPort(ABC):
    @abstractmethod
    async def read_user_by_id(self, *, user_id: UUID) -> User:
        ...

    @abstractmethod
    async def update_user(self, *, user_id: UUID, dto: UpdateUserDTO) -> None:
        ...
