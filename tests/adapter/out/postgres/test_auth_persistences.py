from uuid import uuid4

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from techlog_article.common.database import models

from techlog_article.auth.adapter.out.persistences import (
    UserPersistenceAdapter,
    UserRepository,
    AuthPersistenceAdapter,
    AuthRepository,
    UpdateAuthDTO,
)

from .sqlalchemy_utils import (
    store_single_entity,
    store_user_with_auth,
    read_single_entity_by_field,
    NoResultFoundError,
)


@pytest_asyncio.fixture
def user_persistence_adapter(db_session: AsyncSession) -> UserPersistenceAdapter:
    return UserPersistenceAdapter(user_repository=UserRepository(db_session=db_session))


@pytest_asyncio.fixture
def auth_persistence_adapter(
    db_session: AsyncSession,
) -> AuthPersistenceAdapter:
    return AuthPersistenceAdapter(auth_repository=AuthRepository(db_session=db_session))


@pytest.mark.asyncio
class TestUserPersistenceAdapter:
    async def test_reads_user_by_name(
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

        user = await user_persistence_adapter.read_user_by_name(username=username)
        assert user and user.id == id

        non_existing_user = await user_persistence_adapter.read_user_by_name(
            username="fake"
        )
        assert non_existing_user is None


@pytest.mark.asyncio
class TestAuthPersistenceAdapter:
    async def test_reads_auth_by_user_id(
        self,
        db_session: AsyncSession,
        auth_persistence_adapter: AuthPersistenceAdapter,
    ):
        user_id = uuid4()
        await store_user_with_auth(
            db_session=db_session,
            id=user_id,
            username="test",
            email="email",
            hashed_password="",
        )

        auth = await auth_persistence_adapter.read_auth_by_user_id(user_id=user_id)
        assert auth.user_id == user_id

        non_existing_auth = await auth_persistence_adapter.read_auth_by_user_id(
            user_id=uuid4()
        )
        assert non_existing_auth is None

    async def test_updates_auth(
        self,
        db_session: AsyncSession,
        auth_persistence_adapter: AuthPersistenceAdapter,
    ):
        user_id = uuid4()
        await store_user_with_auth(
            db_session=db_session,
            id=user_id,
            username="test",
            email="email",
            hashed_password="",
        )

        dto = UpdateAuthDTO(access_token="123")
        await auth_persistence_adapter.update_auth(user_id=user_id, dto=dto)

        updated_auth = await read_single_entity_by_field(
            db_session=db_session,
            orm_model=models.Auth,
            field_name="user_id",
            field_value=user_id,
        )
        assert updated_auth.access_token == dto.access_token

    async def test_updates_non_existing_auth(
        self, auth_persistence_adapter: AuthPersistenceAdapter
    ):
        with pytest.raises(NoResultFoundError):
            await auth_persistence_adapter.update_auth(
                user_id=uuid4(), dto=UpdateAuthDTO()
            )
