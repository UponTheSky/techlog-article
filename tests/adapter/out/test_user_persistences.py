from uuid import uuid4

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.techlog_article.common.database import models

from src.techlog_article.user.adapter.out.persistences import (
    UpdateUserDTO,
    CreateUserDTO,
    UserPersistenceAdapter,
    UserAuthPersistenceAdapter,
    UserRepository,
    UserAuthRepository,
)

from .sqlalchemy_utils import (
    store_single_entity,
    db_commit,
    read_single_entity_by_id,
    read_user_with_auth_by_username,
    object_refresh,
)


@pytest_asyncio.fixture
def user_persistence_adapter(db_session: AsyncSession) -> UserPersistenceAdapter:
    return UserPersistenceAdapter(user_repository=UserRepository(db_session=db_session))


@pytest_asyncio.fixture
def user_auth_persistence_adapter(
    db_session: AsyncSession,
) -> UserAuthPersistenceAdapter:
    return UserAuthPersistenceAdapter(
        user_auth_repository=UserAuthRepository(db_session=db_session)
    )


@pytest.mark.asyncio
class TestUserPersistenceAdapter:
    async def test_checks_user_exists(
        self, db_session: AsyncSession, user_persistence_adapter: UserPersistenceAdapter
    ):
        id, username, email = uuid4(), "test", "test@test.com"
        await store_single_entity(
            db_session=db_session,
            orm_model=models.User,
            id=id,
            username=username,
            email=email,
            hashed_password="",
        )

        assert await user_persistence_adapter.check_exists_by_username(username)
        assert await user_persistence_adapter.check_exists_by_email(email)
        assert await user_persistence_adapter.check_exists_by_id(id)

        assert not (await user_persistence_adapter.check_exists_by_username(""))
        assert not (await user_persistence_adapter.check_exists_by_email(""))
        assert not (await user_persistence_adapter.check_exists_by_id(uuid4()))

    async def test_updates_user(
        self, db_session: AsyncSession, user_persistence_adapter: UserPersistenceAdapter
    ):
        id, username, email, hashed_password = uuid4(), "test", "test@test.com", ""
        await store_single_entity(
            db_session=db_session,
            orm_model=models.User,
            id=id,
            username=username,
            email=email,
            hashed_password=hashed_password,
        )

        update_user_dto = UpdateUserDTO(username="new_username", hashed_password="123")
        await user_persistence_adapter.update_user(user_id=id, dto=update_user_dto)
        await db_commit(db_session=db_session)

        updated_user = await read_single_entity_by_id(
            db_session=db_session, orm_model=models.User, id=id
        )

        assert updated_user.username != username
        assert updated_user.hashed_password != hashed_password
        assert updated_user.email == email


@pytest.mark.asyncio
class TestUserAuthPersistenceAdapter:
    async def test_creates_user_with_auth(
        self,
        db_session: AsyncSession,
        user_auth_persistence_adapter: UserAuthPersistenceAdapter,
    ):
        username = "testtest"
        dto = CreateUserDTO(
            username=username, hashed_password="", email="test@test.com"
        )
        await user_auth_persistence_adapter.create_user_with_auth(dto=dto)
        await db_commit(db_session=db_session)

        created_user = await read_user_with_auth_by_username(
            db_session=db_session, username=username
        )
        assert created_user.username == username
        assert created_user.auth is not None

    async def test_deletes_user_with_auth(
        self,
        db_session: AsyncSession,
        user_auth_persistence_adapter: UserAuthPersistenceAdapter,
    ):
        username = "testtest"
        dto = CreateUserDTO(
            username=username, hashed_password="", email="test@test.com"
        )
        await user_auth_persistence_adapter.create_user_with_auth(dto=dto)
        await db_commit(db_session=db_session)

        created_user = await read_user_with_auth_by_username(
            db_session=db_session, username=username
        )

        await user_auth_persistence_adapter.delete_user_auth(user_id=created_user.id)
        await object_refresh(db_session=db_session, object=created_user)
        deleted_user = created_user

        assert deleted_user.deleted_at is not None
        assert deleted_user.auth.deleted_at is not None
