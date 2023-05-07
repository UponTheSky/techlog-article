from abc import ABC, abstractmethod
from uuid import UUID


class DeleteUserAuthPort(ABC):
    @abstractmethod
    async def delete_user_auth(self, *, user_id: UUID) -> None:
        ...
