from typing import Optional
from abc import ABC, abstractmethod
from uuid import UUID

from domain.auth import Auth
from .dto import UpdateAuthDTO


class LoginPort(ABC):
    @abstractmethod
    def read_user(self, *, username: Optional[str], id: Optional[UUID]) -> Auth:
        ...

    @abstractmethod
    def update_auth(self, *, dto: UpdateAuthDTO) -> Auth:
        ...
