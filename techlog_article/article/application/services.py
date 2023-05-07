from typing import final, Annotated, Optional
from uuid import UUID

from fastapi import Depends, HTTPException, status as HTTPStatus
from techlog_article.common.database.utils import transactional

from ..domain import Article

from .port.in_ import (
    CreateArticleInDTO,
    ReadArticleInPort,
    ReadArticleResponse,
    ReadArticleListInDTO,
    SingleArticleInList,
    ReadArticleListResponse,
    UpdateArticleInDTO,
    UpdateArticleInPort,
    DeleteArticleInPort,
)
from .port.out import (
    CreateArticleOutDTO,
    CreateArticleOutPort,
    ReadArticleOutPort,
    UpdateArticleOutDTO,
    UpdateArticleOutPort,
    DeleteArticleOutPort,
)

from ..adapter.out.persistences import (
    ArticleUserPersistenceAdapter,
    ArticlePersistenceAdapter,
)


class _ArticleInDBSanityCheckMixin:
    @staticmethod
    def _article_in_db_sanity_check(
        *, article_in_db: Optional[Article], author_id: UUID
    ) -> None:
        if not article_in_db:
            raise HTTPException(
                status_code=HTTPStatus.HTTP_404_NOT_FOUND, detail="Content not found"
            )

        if article_in_db.author_id != author_id:
            raise HTTPException(
                status_code=HTTPStatus.HTTP_403_FORBIDDEN,
                detail="The user doesn't have the permission to modify this content",
            )

        return None


@final
class CreateArticleService(CreateArticleOutPort):
    def __init__(
        self,
        *,
        create_article_out_port: Annotated[
            CreateArticleOutPort, Depends(ArticleUserPersistenceAdapter)
        ],
    ):
        self._create_article_out_port = create_article_out_port

    @transactional
    async def create_article(self, *, dto: CreateArticleInDTO) -> None:
        await self._create_article_out_port.create_article(
            dto=CreateArticleOutDTO(**dto.dict())
        )

        return None


@final
class ReadArticeService(ReadArticleInPort):
    def __init__(
        self,
        *,
        read_article_out_port: Annotated[
            ReadArticleOutPort, Depends(ArticleUserPersistenceAdapter)
        ],
    ):
        self._read_article_out_port = read_article_out_port

    async def read_article_by_id(self, id: UUID) -> ReadArticleResponse:
        article_with_author = (
            await self._read_article_out_port.read_article_by_id_with_author(id)
        )

        if not article_with_author:
            raise HTTPException(
                status_code=HTTPStatus.HTTP_404_NOT_FOUND, detail="Content not found"
            )

        return ReadArticleResponse(
            title=article_with_author.article.title,
            content=article_with_author.article.content,
            author_name=article_with_author.author.username,
            author_email=article_with_author.author.email,
            created_at=article_with_author.article.created_at,
            updated_at=article_with_author.article.updated_at,
        )

    async def read_article_list(
        self, *, dto: ReadArticleListInDTO
    ) -> ReadArticleListResponse:
        articles_with_authors = (
            await self._read_article_out_port.read_article_with_author_list(
                offset=dto.offset, limit=dto.limit, order_by=dto.order_by
            )
        )
        total_articles_count = (
            await self._read_article_out_port.get_total_articles_count()
        )

        return ReadArticleListResponse(
            total_articles_count=total_articles_count,
            article_list=[
                SingleArticleInList(
                    id=element.article.id,
                    title=element.article.title,
                    author_name=element.author.username,
                    created_at=element.article.created_at,
                    updated_at=element.article.created_at,
                )
                for element in articles_with_authors
            ],
        )


@final
class UpdateArticeService(UpdateArticleInPort, _ArticleInDBSanityCheckMixin):
    def __init__(
        self,
        *,
        update_article_out_port: Annotated[
            UpdateArticleOutPort, Depends(ArticlePersistenceAdapter)
        ],
    ):
        self._update_article_out_port = update_article_out_port

    @transactional
    async def update_article(
        self, *, author_id: UUID, article_id: UUID, dto: UpdateArticleInDTO
    ) -> None:
        article_in_db = await self._update_article_out_port.read_article_by_id(
            article_id
        )

        self._article_in_db_sanity_check(
            article_in_db=article_in_db, author_id=author_id
        )

        await self._update_article_out_port.update_article(
            article_id=article_id,
            dto=UpdateArticleOutDTO(**dto.dict(exclude_unset=True)),
        )

        return None


@final
class DeleteArticleService(DeleteArticleInPort, _ArticleInDBSanityCheckMixin):
    def __init__(
        self,
        *,
        delete_article_out_port: Annotated[
            DeleteArticleOutPort, Depends(ArticlePersistenceAdapter)
        ],
    ):
        self._delete_article_out_port = delete_article_out_port

    @transactional
    async def delete_article(self, *, author_id: UUID, article_id: UUID) -> None:
        article_in_db = await self._delete_article_out_port.read_article_by_id(
            article_id
        )

        self._article_in_db_sanity_check(
            article_in_db=article_in_db, author_id=author_id
        )

        await self._delete_article_out_port.delete_article(article_id=article_id)

        return None
