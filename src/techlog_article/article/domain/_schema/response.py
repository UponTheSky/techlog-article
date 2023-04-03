from uuid import UUID, uuid4
from datetime import datetime

from pydantic import Field

from common.schema.article import ArticleCore as _ArticleCore


class ArticleResponse(_ArticleCore):
    author_id: UUID = Field(description="The id field of 'User' class")

    class Config:
        schema_extra = {
            "example": {
                "id": str(uuid4()),
                "title": "How to use FastAPI",
                "content": "# TL;DR ...",
                "created_at": str(datetime.now()),
                "updated_at": str(datetime.now()),
            }
        }
