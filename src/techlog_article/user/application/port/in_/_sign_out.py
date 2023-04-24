from abc import ABC, abstractmethod
from uuid import UUID


class SignOutPort(ABC):
    @abstractmethod
    async def sign_out(self, *, user_id: UUID) -> None:
        ...
