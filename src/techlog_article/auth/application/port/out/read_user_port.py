from typing import Optional
from abc import ABC, abstractmethod
from uuid import UUID

from domain.user import User


class ReadUserPort(ABC):
    @abstractmethod
    def read_user(
        self, *, username: Optional[str], id: Optional[UUID]
    ) -> Optional[User]:
        ...
