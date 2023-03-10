from uuid import UUID

from pydantic import Field

from common.schema.article import ArticleCore as _ArticleCore


class ArticleResponse(_ArticleCore):
    author_id: UUID = Field(description="The id field of 'User' class")
