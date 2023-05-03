from abc import ABC, abstractmethod
from uuid import UUID


class CheckUserPort(ABC):
    @abstractmethod
    async def check_exists_by_username(self, username: str) -> bool:
        ...

    @abstractmethod
    async def check_exists_by_email(self, email: str) -> bool:
        ...

    @abstractmethod
    async def check_exists_by_id(self, id: UUID) -> bool:
        ...
