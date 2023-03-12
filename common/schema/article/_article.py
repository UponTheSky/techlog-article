from typing import Optional
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field

from common.schema.user import User


class ArticleCore(BaseModel):
    title: str
    content: str

    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]


class Article(ArticleCore):
    id: UUID = Field(
        description="The primary key that is automatically generated from the DB"
    )
    author: User
