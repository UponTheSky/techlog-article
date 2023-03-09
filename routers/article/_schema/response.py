from uuid import UUID

from common.article import ArticleCore


class ArticleResponse(ArticleCore):
    author_id: UUID
