from abc import ABC, abstractmethod

from domain.auth import Auth
from .dto import UpdateAuthDTO


class LogoutPort(ABC):
    @abstractmethod
    def update_auth(self, *, dto: UpdateAuthDTO) -> Auth:
        ...
