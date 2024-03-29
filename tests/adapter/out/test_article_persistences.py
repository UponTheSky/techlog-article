from uuid import uuid4
from datetime import datetime

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from techlog_article.common.database import models

from techlog_article.article.adapter.out.persistences import (
    ArticleUserPersistenceAdapter,
    ArticleUserRepository,
    ArticlePersistenceAdapter,
    ArticleRepository,
    CreateArticleOutDTO,
    UpdateArticleOutDTO,
)

from .sqlalchemy_utils import (
    db_commit,
    read_single_entity_by_id,
    store_single_entity,
    store_user_with_article,
    read_single_entity_by_field,
    NoResultFoundError,
)


@pytest_asyncio.fixture
def article_user_persistence_adapter(
    db_session: AsyncSession,
) -> ArticleUserPersistenceAdapter:
    return ArticleUserPersistenceAdapter(
        article_user_repository=ArticleUserRepository(db_session=db_session)
    )


@pytest_asyncio.fixture
def article_persistence_adapter(
    db_session: AsyncSession,
) -> ArticlePersistenceAdapter:
    return ArticlePersistenceAdapter(
        article_repository=ArticleRepository(db_session=db_session)
    )


@pytest.mark.asyncio
class TestArticleUserPersistenceAdapter:
    async def test_creates_article(
        self,
        db_session: AsyncSession,
        article_user_persistence_adapter: ArticleUserPersistenceAdapter,
    ):
        user_id = uuid4()
        await store_single_entity(
            db_session=db_session,
            orm_model=models.User,
            id=user_id,
            username="",
            email="",
            hashed_password="",
        )

        await article_user_persistence_adapter.create_article(
            dto=CreateArticleOutDTO(title="123", author_id=user_id)
        )
        await db_commit(db_session=db_session)

        article: models.Article = await read_single_entity_by_field(
            db_session=db_session,
            orm_model=models.Article,
            field_name="author_id",
            field_value=user_id,
        )
        assert article and article.author_id == user_id

    async def test_creates_article_of_nonexisting_user(
        self, article_user_persistence_adapter: ArticleUserPersistenceAdapter
    ):
        with pytest.raises(NoResultFoundError):
            await article_user_persistence_adapter.create_article(
                dto=CreateArticleOutDTO(title="123", author_id=uuid4())
            )

    async def test_reads_article_with_author(
        self,
        db_session: AsyncSession,
        article_user_persistence_adapter: ArticleUserPersistenceAdapter,
    ):
        user_id, article_id = uuid4(), uuid4()
        await store_user_with_article(
            db_session=db_session,
            user_id=user_id,
            username="",
            article_id=article_id,
            article_title="",
        )

        user_with_article = (
            await article_user_persistence_adapter.read_article_by_id_with_author(
                article_id
            )
        )
        assert user_with_article is not None
        assert user_with_article.article.id == article_id
        assert user_with_article.author.id == user_id

        non_existing_user_with_article = (
            await article_user_persistence_adapter.read_article_by_id_with_author(
                uuid4()
            )
        )
        assert non_existing_user_with_article is None

    async def test_reads_deleted_article_with_author(
        self,
        db_session: AsyncSession,
        article_user_persistence_adapter: ArticleUserPersistenceAdapter,
    ):
        article_id = uuid4()
        await store_user_with_article(
            db_session=db_session,
            user_id=uuid4(),
            username="",
            article_id=article_id,
            article_title="",
            article_deleted_at=datetime.now(),
        )

        assert (
            await article_user_persistence_adapter.read_article_by_id_with_author(
                article_id
            )
        ) is None

    async def test_reads_article_with_deleted_author(
        self,
        db_session: AsyncSession,
        article_user_persistence_adapter: ArticleUserPersistenceAdapter,
    ):
        article_id = uuid4()
        await store_user_with_article(
            db_session=db_session,
            user_id=uuid4(),
            username="",
            article_id=article_id,
            article_title="",
            user_deleted_at=datetime.now(),
        )

        assert (
            await article_user_persistence_adapter.read_article_by_id_with_author(
                article_id
            )
        ) is None

    async def test_reads_article_list(
        self,
        db_session: AsyncSession,
        article_user_persistence_adapter: ArticleUserPersistenceAdapter,
    ):
        number = 2
        for index in range(number):
            await store_user_with_article(
                db_session=db_session,
                user_id=uuid4(),
                username=str(index),
                article_id=uuid4(),
                article_title=str(index),
            )

        article_with_user_list = (
            await article_user_persistence_adapter.read_article_with_author_list(
                offset=0, limit=5, order_by="created_at"
            )
        )
        assert len(article_with_user_list) == number

    async def test_gets_total_articles_count(
        self,
        db_session: AsyncSession,
        article_user_persistence_adapter: ArticleUserPersistenceAdapter,
    ):
        number = 2
        for index in range(number):
            await store_user_with_article(
                db_session=db_session,
                user_id=uuid4(),
                username="",
                article_id=uuid4(),
                article_title=str(index),
            )

        article_count = (
            await article_user_persistence_adapter.get_total_articles_count()
        )
        assert article_count == number


@pytest.mark.asyncio
class TestArticlePersistenceAdapter:
    async def test_reads_article_by_id(
        self,
        db_session: AsyncSession,
        article_persistence_adapter: ArticlePersistenceAdapter,
    ):
        id = uuid4()
        await store_user_with_article(
            db_session=db_session,
            user_id=uuid4(),
            username="",
            article_id=id,
            article_title="",
        )

        article = await article_persistence_adapter.read_article_by_id(id)
        assert article.id == id

        assert (await article_persistence_adapter.read_article_by_id(uuid4())) is None

    async def test_updates_article(
        self,
        db_session: AsyncSession,
        article_persistence_adapter: ArticlePersistenceAdapter,
    ):
        id, new_title, content = uuid4(), "42", "content"
        dto = UpdateArticleOutDTO(title=new_title)

        await store_user_with_article(
            db_session=db_session,
            user_id=uuid4(),
            username="",
            article_id=id,
            article_title="",
            content=content,
        )

        await article_persistence_adapter.update_article(article_id=id, dto=dto)
        await db_commit(db_session=db_session)

        article = await read_single_entity_by_id(
            db_session=db_session, orm_model=models.Article, id=id
        )

        assert article.title == new_title
        assert article.content == content

    async def test_updates_non_existing_article(
        self,
        article_persistence_adapter: ArticlePersistenceAdapter,
    ):
        with pytest.raises(NoResultFoundError):
            await article_persistence_adapter.update_article(
                article_id=uuid4(), dto=UpdateArticleOutDTO()
            )

    async def test_deletes_article(
        self,
        db_session: AsyncSession,
        article_persistence_adapter: ArticlePersistenceAdapter,
    ):
        id = uuid4()
        await store_user_with_article(
            db_session=db_session,
            user_id=uuid4(),
            username="",
            article_id=id,
            article_title="",
        )

        await article_persistence_adapter.delete_article(article_id=id)

        deleted_article = await read_single_entity_by_id(
            db_session=db_session, orm_model=models.Article, id=id
        )
        assert deleted_article.deleted_at is not None

    async def test_deletes_non_existing_article(
        self,
        article_persistence_adapter: ArticlePersistenceAdapter,
    ):
        with pytest.raises(NoResultFoundError):
            await article_persistence_adapter.delete_article(article_id=uuid4())
