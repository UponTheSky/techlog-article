from typing import Optional
from abc import ABC, abstractmethod
from uuid import UUID

from pydantic import BaseModel, validator


class UpdateArticleInDTO(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

    @validator("title")
    def title_is_valid(cls, v):
        if not v:  # including empty string; excluded from the DAO in the out adapter
            return None

        if not (1 <= len(v) <= 32):
            raise ValueError("The title must be of length from 1 to 32")

        return v


class UpdateArticleInPort(ABC):
    @abstractmethod
    async def update_article(
        self, *, article_id: UUID, dto: UpdateArticleInDTO
    ) -> None:
        ...
