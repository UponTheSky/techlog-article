from abc import ABC, abstractmethod
from uuid import UUID


class DeleteArticleOutPort(ABC):
    @abstractmethod
    async def delete_article(self, *, article_id: UUID) -> None:
        ...
