from typing import Optional
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field

from common.schema.user import User


class ArticleBase(BaseModel):
    title: Optional[str]
    content: Optional[str]


class ArticleCore(BaseModel):
    id: UUID = Field(
        description="The primary key that is automatically generated from the DB"
    )
    title: str
    content: str

    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None


class Article(ArticleCore):
    author: User
