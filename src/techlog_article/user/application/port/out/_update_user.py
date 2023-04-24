from typing import Optional
from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID


@dataclass
class UpdateUserDTO:
    username: Optional[str]
    email: Optional[str]
    hashed_password: Optional[str]


class UpdateUserPort(ABC):
    @abstractmethod
    async def update_user(self, *, user_id: UUID, dto: UpdateUserDTO) -> None:
        ...
