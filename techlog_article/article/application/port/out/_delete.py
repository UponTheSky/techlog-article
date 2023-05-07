from typing import Optional
from abc import ABC, abstractmethod
from uuid import UUID

from ....domain import Article


class DeleteArticleOutPort(ABC):
    @abstractmethod
    async def read_article_by_id(self, id: UUID) -> Optional[Article]:
        ...

    @abstractmethod
    async def delete_article(self, *, article_id: UUID) -> None:
        ...
