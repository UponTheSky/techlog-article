from abc import ABC, abstractmethod
from uuid import UUID


class DeleteArticleInPort(ABC):
    @abstractmethod
    async def delete_article(self, *, author_id: UUID, article_id: UUID) -> None:
        ...
