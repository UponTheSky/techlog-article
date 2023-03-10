from uuid import UUID

from pydantic import BaseModel, Field

from common.schema.article import ArticleBase as _ArticleBase


class CreateArticle(_ArticleBase):
    title: str = Field(
        description="The article's title should be non-empty when created", min_length=1
    )
    content: str = ""
    author_id: UUID = Field(description="The id field of the 'User' class")


class ReadArticle(BaseModel):
    id: UUID = Field(description="The id of the article")


class UpdateArticle(_ArticleBase):
    id: UUID = Field(description="The id of the article")


class DeleteArticle(BaseModel):
    id: UUID = Field(description="The id of the article")
