import os

import pytest_asyncio
from testcontainers.postgres import PostgresContainer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from techlog_article.common.database._session import get_session_manager
from techlog_article.common.database import models
from techlog_article.common.config import config

# reference: https://mariogarcia.github.io/blog/2019/10/pytest_fixtures.html

POSTGRES_VERSION = "15.0"

session_manager = get_session_manager()


@pytest_asyncio.fixture(scope="session")
async def db_session():
    container = PostgresContainer(f"postgres:{POSTGRES_VERSION}")
    container.start()

    # db setup
    original_db_url = os.environ.get("DB_URL", "")
    os.environ["DB_URL"] = container.get_connection_url()

    # table setup
    # in order to use models.Base.metadata.create_all, we have to use connection
    # instead of the session
    # see the examples in: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
    postgres_engine = create_async_engine(url=config.DB_URL)

    async with postgres_engine.begin() as connection:
        await connection.run_sync(models.Base.metadata.create_all)

    # get the session(setting the context should occur beforehand)
    session_manager.set_db_session_context(session_id=42)
    current_session = session_manager.get_current_session()

    yield current_session

    await current_session.close()
    os.environ["DB_URL"] = original_db_url
    container.stop()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def clean_up(db_session: AsyncSession):
    for table in reversed(models.Base.metadata.sorted_tables):
        await db_session.execute(table.delete())
