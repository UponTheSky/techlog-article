from typing import Optional
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel

from common.user import User


class ArticleCore(BaseModel):
    id: UUID
    title: str
    content: str

    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]


class Article(ArticleCore):
    author: User
