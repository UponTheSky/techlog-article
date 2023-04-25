from typing import Optional
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from user.domain.user import User


class Article(BaseModel):
    id: UUID
    title: str
    content: str
    author: User

    created_at: datetime
    updated_at: Optional[datetime]
