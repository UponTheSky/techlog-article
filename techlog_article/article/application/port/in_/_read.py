from typing import Optional
from abc import ABC, abstractmethod
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field, validator

from ....domain import Article


class ReadArticleResponse(BaseModel):
    title: str
    content: Optional[str] = None
    author_name: str
    author_email: str
    created_at: datetime
    updated_at: Optional[datetime] = None


class ReadArticleListInDTO(BaseModel):
    offset: int = Field(default=0, ge=0)
    limit: int = Field(default=1, ge=1)
    order_by: str = Field(
        default="created_at", description="Must be a field of the Article schema"
    )

    @validator("order_by")
    def validate_order_by(cls, v):
        if v not in set(Article.__fields__):
            raise ValueError(
                "The sort criterion should be one of the fields in the Article schema"
            )

        return v


class SingleArticleInList(BaseModel):
    id: UUID
    title: str
    author_name: str
    created_at: datetime
    updated_at: Optional[datetime] = None


class ReadArticleListResponse(BaseModel):
    total_articles_count: int
    article_list: list[SingleArticleInList]


class ReadArticleInPort(ABC):
    @abstractmethod
    async def read_article_by_id(self, id: UUID) -> ReadArticleResponse:
        ...

    @abstractmethod
    async def read_article_list(
        self, *, dto: ReadArticleListInDTO
    ) -> ReadArticleListResponse:
        ...
