from typing import Optional
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Article(BaseModel):
    id: UUID
    title: str
    content: str
    author_id: UUID

    created_at: datetime
    updated_at: Optional[datetime]
