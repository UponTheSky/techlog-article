import pytest_asyncio
from testcontainers.mongodb import MongoDbContainer
from pymongo.database import Database as Session

from techlog_article.common.database._session import get_session_manager

session_manager = get_session_manager()


async def db_session():
    container = MongoDbContainer("mongodb:latest")
    client = container.get_connection_client()
    session = client.test_db

    # collection(table) setup -> not required for the firestore DB testing

    yield session

    client.close()
    container.stop()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def clean_up(db_session: Session):
    collection_names = db_session.list_collection_names()

    for name in collection_names:
        db_session.drop_collection(name)
