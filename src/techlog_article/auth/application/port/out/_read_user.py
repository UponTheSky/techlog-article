from typing import Optional
from abc import ABC, abstractmethod

from user.domain.user import User


class ReadUserPort(ABC):
    @abstractmethod
    async def read_user_by_name(self, *, username: str) -> Optional[User]:
        ...
