from typing import Optional

from pydantic import BaseModel


class CreateArticleBody(BaseModel):
    title: str
    content: Optional[str] = None
    thumbnail_url: Optional[str] = None
