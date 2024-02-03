import pytest_asyncio
from testcontainers.mongodb import MongoDbContainer
from pymongo import MongoClient

from techlog_article.common.database._session import get_session_manager

session_manager = get_session_manager()


@pytest_asyncio.fixture(scope="session")
async def db_client():
    # since we don't have firestore testcontainer, we use mongodb instead
    container = MongoDbContainer("mongodb:latest")
    client = container.get_connection_client()

    # collection(table) setup -> not required for the firestore DB testing
    yield client

    client.close()
    container.stop()


@pytest_asyncio.fixture(scope="session")
async def db_instance(db_client: MongoClient):
    return getattr(db_client, "test_db")


@pytest_asyncio.fixture(scope="function")
async def db_session(db_client: MongoClient):
    session = db_client.start_session()

    yield session

    session.end_session()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def clean_up(db_client: MongoClient):
    collection_names = db_client.test_db.list_collection_names()

    for name in collection_names:
        db_client.test_db.drop_collection(name)
