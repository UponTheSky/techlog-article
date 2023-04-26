from typing import Optional
from abc import ABC, abstractmethod
from uuid import UUID

from pydantic import BaseModel


class UpdateArticleOutDTO(BaseModel):
    title: Optional[str]
    content: Optional[str]


class UpdateArticleOutPort(ABC):
    @abstractmethod
    async def update_article(
        self, *, article_id: UUID, dto: UpdateArticleOutDTO
    ) -> None:
        ...
