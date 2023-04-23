from typing import Optional
from abc import ABC, abstractmethod
from uuid import UUID

from pydantic import BaseModel


class UpdateAuthDTO(BaseModel):
    user_id: UUID
    access_token: Optional[str]


class UpdateAuthPort(ABC):
    @abstractmethod
    async def update_auth(self, *, dto: UpdateAuthDTO) -> None:
        ...
