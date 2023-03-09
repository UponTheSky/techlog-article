from uuid import UUID
from wsgiref.validate import validator

from pydantic import BaseModel

from common.article import ArticleBase


class CreateArticle(ArticleBase):
    title: str
    content: str = ""
    author_id: UUID

    @validator
    def title_non_empty(cls, v):
        if len(v) == 0:
            raise ValueError("An article's title should be of length greator than 0")
        return v


class ReadArticle(BaseModel):
    id: UUID


class UpdateArticle(ArticleBase):
    id: UUID


class DeleteArticle(BaseModel):
    id: UUID
