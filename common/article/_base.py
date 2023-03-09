from typing import Optional

from pydantic import BaseModel


class ArticleBase(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
