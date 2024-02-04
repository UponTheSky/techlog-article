from uuid import uuid4

import pytest
import pytest_asyncio

from pymongo.database import Database
from pymongo.client_session import ClientSession

from techlog_article.auth.adapter.out.persistences import (
    UserPersistenceAdapter,
    UserRepository,
    AuthPersistenceAdapter,
    AuthRepository,
    UpdateAuthDTO,
)

from .utils import (
    store_single_entity,
    store_user_with_auth,
    read_single_entity_by_field,
    db_commit,
)


@pytest_asyncio.fixture
def user_persistence_adapter(db_instance: Database) -> UserPersistenceAdapter:
    return UserPersistenceAdapter(
        user_repository=UserRepository(db_instance=db_instance)
    )


@pytest_asyncio.fixture
def auth_persistence_adapter(
    db_instance: Database,
) -> AuthPersistenceAdapter:
    return AuthPersistenceAdapter(
        auth_repository=AuthRepository(db_instance=db_instance)
    )


@pytest.mark.asyncio
class TestUserPersistenceAdapter:
    async def test_reads_user_by_name(
        self,
        db_instance: Database,
        db_session: ClientSession,
        user_persistence_adapter: UserPersistenceAdapter,
    ):
        id, username, email = uuid4(), "test", "test@test.com"
        store_single_entity(
            db_instance=db_instance,
            db_session=db_session,
            collection_name="user",
            document={
                "id": str(id),
                "username": username,
                "email": email,
                "hashed_password": "",
                "auth": {},
            },
        )

        user = await user_persistence_adapter.read_user_by_name(username=username)
        assert user and user.id == id

        non_existing_user = await user_persistence_adapter.read_user_by_name(
            username="fake"
        )
        assert non_existing_user is None


@pytest.mark.asyncio
@pytest
class TestAuthPersistenceAdapter:
    async def test_updates_auth(
        self,
        db_instance: Database,
        db_session: ClientSession,
        auth_persistence_adapter: AuthPersistenceAdapter,
    ):
        user_id = uuid4()
        store_user_with_auth(
            db_instance=db_instance,
            db_session=db_session,
            user_id=user_id,
            username="test",
            email="email",
            hashed_password="",
            auth={"access_token": "not_updated"},
        )

        dto = UpdateAuthDTO(access_token="123")
        await auth_persistence_adapter.update_auth(user_id=user_id, dto=dto)
        db_commit(db_session=db_session)

        user = await read_single_entity_by_field(
            db_instance=db_instance,
            collection_name="user",
            field_name="id",
            field_value=user_id,
        )
        assert user.get("auth") and (
            user.get("auth").get("access_token") == dto.access_token
        )

    async def test_updates_non_existing_auth(
        self, auth_persistence_adapter: AuthPersistenceAdapter
    ):
        with pytest.raises(NoResultFoundError):  # noqa F821
            await auth_persistence_adapter.update_auth(
                user_id=uuid4(), dto=UpdateAuthDTO()
            )
