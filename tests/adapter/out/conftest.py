import os

import pytest_asyncio
from testcontainers.postgres import PostgresContainer
from sqlalchemy.ext.asyncio import AsyncSession

from techlog_article.common.database._session import (
    get_current_session,
    set_db_session_context,
    engine,
)
from techlog_article.common.database import models

# reference: https://mariogarcia.github.io/blog/2019/10/pytest_fixtures.html

POSTGRES_VERSION = "15.0"


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup():
    container = PostgresContainer(f"postgres:{POSTGRES_VERSION}")
    container.start()

    # db setup
    original_db_url = os.environ.get("DB_URL", "")
    os.environ["DB_URL"] = container.get_connection_url()

    # table setup
    # in order to use models.Base.metadata.create_all, we have to use connection
    # instead of the session
    # see the examples in: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
    async with engine.begin() as connection:
        await connection.run_sync(models.Base.metadata.create_all)

        yield

        os.environ["DB_URL"] = original_db_url
        container.stop()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def db_session():
    # get the session(setting the context should occur beforehand)
    set_db_session_context(session_id=42)
    current_session = get_current_session()

    yield current_session

    await current_session.close()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def clean_up(db_session: AsyncSession):
    for table in reversed(models.Base.metadata.sorted_tables):
        await db_session.execute(table.delete())
