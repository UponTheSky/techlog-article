from typing import Optional
from abc import ABC, abstractmethod
from uuid import UUID

from pydantic import BaseModel

from ....domain import Auth


class UpdateAuthDTO(BaseModel):
    access_token: Optional[str] = None


class UpdateAuthPort(ABC):
    @abstractmethod
    async def update_auth(self, *, user_id: UUID, dto: UpdateAuthDTO) -> None:
        ...


class ReadAuthPort(ABC):
    @abstractmethod
    async def read_auth_by_user_id(self, *, user_id: UUID) -> Optional[Auth]:
        ...
