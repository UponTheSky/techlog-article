from typing import Optional
from abc import ABC, abstractmethod
from uuid import UUID

from pydantic import BaseModel, Field


class CreateArticleInDTO(BaseModel):
    title: str = Field(
        min_length=1, max_length=32, description="The title is of length from 1 to 32"
    )
    content: Optional[str] = None
    thumbnail_url: Optional[str] = None
    author_id: UUID = Field(description="A user's user_id(=User.id)")


class CreateArticleOutPort(ABC):
    @abstractmethod
    async def create_article(self, *, dto: CreateArticleInDTO) -> None:
        ...
