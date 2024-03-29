from typing import Optional
from abc import ABC, abstractmethod
from uuid import UUID

from pydantic import BaseModel

from ....domain import Article


class UpdateArticleOutDTO(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    thumbnail_url: Optional[str] = None


class UpdateArticleOutPort(ABC):
    @abstractmethod
    async def read_article_by_id(self, id: UUID) -> Optional[Article]:
        ...

    @abstractmethod
    async def update_article(
        self, *, article_id: UUID, dto: UpdateArticleOutDTO
    ) -> None:
        ...
