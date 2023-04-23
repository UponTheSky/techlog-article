from abc import ABC, abstractmethod
from uuid import UUID


class LogoutPort(ABC):
    @abstractmethod
    async def logout(self, *, user_id: UUID) -> None:
        ...
