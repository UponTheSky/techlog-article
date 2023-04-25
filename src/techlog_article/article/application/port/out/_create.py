from typing import Optional
from abc import ABC, abstractmethod
from uuid import UUID

from pydantic import BaseModel


class CreateArticleOutDTO(BaseModel):
    title: str
    content: Optional[str] = None
    author_id: UUID


class CreateArticleOutPort(ABC):
    @abstractmethod
    async def create_article(self, *, dto: CreateArticleOutDTO) -> None:
        ...
