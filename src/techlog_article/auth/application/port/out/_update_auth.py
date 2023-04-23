from abc import ABC, abstractmethod
from uuid import UUID

from pydantic import BaseModel


class UpdateAuthDTO(BaseModel):
    user_id: UUID
    access_token: str


class UpdateAuthPort(ABC):
    @abstractmethod
    def update_auth(self, *, dto: UpdateAuthDTO) -> None:
        ...
