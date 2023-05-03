from uuid import uuid4

import pytest
import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.techlog_article.common.database import models

from . import (
    UpdateUserDTO,
    CreateUserDTO,
    UserPersistenceAdapter,
    UserAuthPersistenceAdapter,
    UserRepository,
    UserAuthRepository,
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
        db_session.add(
            models.User(id=id, username=username, email=email, hashed_password="")
        )
        await db_session.commit()

        assert await user_persistence_adapter.check_exists_by_username(username)
        assert await user_persistence_adapter.check_exists_by_email(email)
        assert await user_persistence_adapter.check_exists_by_id(id)

    async def test_updates_user(
        self, db_session: AsyncSession, user_persistence_adapter: UserPersistenceAdapter
    ):
        id, username, email, hashed_password = uuid4(), "test", "test@test.com", ""
        db_session.add(
            models.User(
                id=id, username=username, email=email, hashed_password=hashed_password
            )
        )
        await db_session.commit()

        update_user_dto = UpdateUserDTO(username="new_username", hashed_password="123")
        await user_persistence_adapter.update_user(user_id=id, dto=update_user_dto)
        await db_session.commit()

        updated_user = await db_session.scalar(
            select(models.User).where(models.User.id == id)
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
        await db_session.commit()

        created_user = await db_session.scalar(
            select(models.User)
            .options(selectinload(models.User.auth))
            .where(models.User.username == username)
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
        await db_session.commit()

        created_user = await db_session.scalar(
            select(models.User)
            .options(selectinload(models.User.auth))
            .where(models.User.username == username)
        )

        await user_auth_persistence_adapter.delete_user_auth(user_id=created_user.id)
        await db_session.refresh(created_user)
        deleted_user = created_user

        assert deleted_user.deleted_at is not None
        assert deleted_user.auth.deleted_at is not None
