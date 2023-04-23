from typing import Optional
from abc import ABC, abstractmethod
from uuid import UUID

from common.utils.message import ServiceMessage


class LogoutPort(ABC):
    @abstractmethod
    def logout(self, *, user_id: UUID) -> ServiceMessage[Optional[str]]:
        ...
