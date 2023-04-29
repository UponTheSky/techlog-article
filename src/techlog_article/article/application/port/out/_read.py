from typing import Optional
from abc import ABC, abstractmethod
from uuid import UUID
from dataclasses import dataclass

from ....domain import Article
from src.techlog_article.user import User


@dataclass
class ArticleWithAuthor:
    article: Article
    author: User


class ReadArticleOutPort(ABC):
    @abstractmethod
    async def read_article_by_id_with_author(
        self, id: UUID
    ) -> Optional[ArticleWithAuthor]:
        ...

    @abstractmethod
    async def read_article_list(
        self, *, offset: int, limit: int, order_by: str
    ) -> list[ArticleWithAuthor]:
        ...

    @abstractmethod
    async def get_total_articles_count(self) -> int:
        ...
