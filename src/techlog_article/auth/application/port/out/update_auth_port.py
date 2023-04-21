from abc import ABC, abstractmethod

from .dto import UpdateAuthDTO


class UpdateAuthPort(ABC):
    @abstractmethod
    def update_auth(self, *, dto: UpdateAuthDTO) -> None:
        ...
