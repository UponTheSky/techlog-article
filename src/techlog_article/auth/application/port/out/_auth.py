from typing import Optional
from abc import ABC, abstractmethod
from uuid import UUID

from pydantic import BaseModel

from domain.auth import Auth


class UpdateAuthDTO(BaseModel):
    user_id: UUID
    access_token: Optional[str]


class UpdateAuthPort(ABC):
    @abstractmethod
    async def update_auth(self, *, dto: UpdateAuthDTO) -> None:
        ...


class ReadAuthPort(ABC):
    @abstractmethod
    async def read_auth_by_user_id(self, *, user_id: UUID) -> Optional[Auth]:
        ...
