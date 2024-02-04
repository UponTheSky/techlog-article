from uuid import uuid4

import pytest
import pytest_asyncio

from pymongo.database import Database
from pymongo.client_session import ClientSession

from techlog_article.user.adapter.out.persistences import (
    UpdateUserDTO,
    CreateUserDTO,
    UserPersistenceAdapter,
    UserAuthPersistenceAdapter,
    UserRepository,
    UserAuthRepository,
)

from .utils import (
    store_single_entity,
    db_commit,
    read_single_entity_by_id,
    read_user_with_auth_by_username,
)


@pytest_asyncio.fixture
def user_persistence_adapter(db_instance: Database) -> UserPersistenceAdapter:
    return UserPersistenceAdapter(
        user_repository=UserRepository(db_instance=db_instance)
    )


@pytest_asyncio.fixture
def user_auth_persistence_adapter(
    db_instance: Database,
) -> UserAuthPersistenceAdapter:
    return UserAuthPersistenceAdapter(
        user_auth_repository=UserAuthRepository(db_instance=db_instance)
    )


@pytest.mark.asyncio
class TestUserPersistenceAdapter:
    async def test_checks_user_exists(
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
                "id": id,
                "username": username,
                "email": email,
                "hashed_password": "",
                "auth": {},
            },
        )

        assert await user_persistence_adapter.check_exists_by_username(username)
        assert await user_persistence_adapter.check_exists_by_email(email)
        assert await user_persistence_adapter.check_exists_by_id(id)

        assert not (await user_persistence_adapter.check_exists_by_username(""))
        assert not (await user_persistence_adapter.check_exists_by_email(""))
        assert not (await user_persistence_adapter.check_exists_by_id(uuid4()))

    async def test_updates_user(
        self,
        db_instance: Database,
        db_session: ClientSession,
        user_persistence_adapter: UserPersistenceAdapter,
    ):
        id, username, email, hashed_password = uuid4(), "test", "test@test.com", ""
        store_single_entity(
            db_instance=db_instance,
            db_session=db_session,
            collection_name="user",
            document={
                "id": id,
                "username": username,
                "email": email,
                "hashed_password": hashed_password,
                "auth": {},
            },
        )

        update_user_dto = UpdateUserDTO(username="new_username", hashed_password="123")
        await user_persistence_adapter.update_user(user_id=id, dto=update_user_dto)
        db_commit(db_session=db_session)

        updated_user = await read_single_entity_by_id(
            db_instance=db_instance, collection_name="user", id=id
        )

        assert updated_user.get("username") != username
        assert updated_user.get("hashed_password") != hashed_password
        assert updated_user.get("email") == email

    async def test_updates_non_existing_user(
        self, user_persistence_adapter: UserPersistenceAdapter
    ):
        with pytest.raises(NoResultFoundError):  # noqa F821
            await user_persistence_adapter.update_user(
                user_id=uuid4(), dto=UpdateUserDTO()
            )


@pytest.mark.asyncio
class TestUserAuthPersistenceAdapter:
    async def test_creates_user_with_auth(
        self,
        db_instance: Database,
        db_session: ClientSession,
        user_auth_persistence_adapter: UserAuthPersistenceAdapter,
    ):
        username = "testtest"
        dto = CreateUserDTO(
            username=username, hashed_password="", email="test@test.com"
        )
        await user_auth_persistence_adapter.create_user_with_auth(dto=dto)
        db_commit(db_session=db_session)

        created_user = await read_user_with_auth_by_username(
            db_instance=db_instance, username=username
        )
        assert created_user.username == username
        assert len(created_user.auth) > 0

    async def test_deletes_user_with_auth(
        self,
        db_instance: Database,
        db_session: ClientSession,
        user_auth_persistence_adapter: UserAuthPersistenceAdapter,
    ):
        username = "testtest"
        dto = CreateUserDTO(
            username=username, hashed_password="", email="test@test.com"
        )
        await user_auth_persistence_adapter.create_user_with_auth(dto=dto)
        db_commit(db_session=db_session)

        created_user = await read_user_with_auth_by_username(
            db_instance=db_instance, username=username
        )

        await user_auth_persistence_adapter.delete_user_auth(user_id=created_user.id)
        db_commit(db_session=db_session)

        deleted_user = read_single_entity_by_id(
            db_instance=db_instance, collection_name="user", id=created_user.id
        )

        assert deleted_user.get("deleted_at") is not None

    async def tests_deletes_non_existing_user(
        self, user_auth_persistence_adapter: UserAuthPersistenceAdapter
    ):
        with pytest.raises(NoResultFoundError):  # noqa F821
            await user_auth_persistence_adapter.delete_user_auth(user_id=uuid4())
