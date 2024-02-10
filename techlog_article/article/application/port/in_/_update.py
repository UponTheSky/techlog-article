from typing import Optional
from abc import ABC, abstractmethod
from uuid import UUID

from pydantic import BaseModel, validator

from ._validation_helper import validate_title


class UpdateArticleInDTO(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    thumbnail_url: Optional[str] = None

    @validator("title")
    def title_is_valid(cls, v):
        if not v:  # including empty string; excluded from the DAO in the out adapter
            return None

        return validate_title(title=v)


class UpdateArticleInPort(ABC):
    @abstractmethod
    async def update_article(
        self, *, author_id: UUID, article_id: UUID, dto: UpdateArticleInDTO
    ) -> None:
        ...
