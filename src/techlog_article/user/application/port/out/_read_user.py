from abc import ABC, abstractmethod


class CheckUserPort(ABC):
    @abstractmethod
    async def check_exists_by_username(self, username: str) -> bool:
        ...

    @abstractmethod
    async def check_exists_by_email(self, email: str) -> bool:
        ...
