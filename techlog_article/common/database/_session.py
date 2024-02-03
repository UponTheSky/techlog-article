from typing import Optional, Callable
from contextvars import ContextVar
import functools

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_scoped_session,
    async_sessionmaker,
    AsyncSession,
    AsyncEngine,
)

from google.cloud import firestore

from ..config import config, gcp_infra_config

# some hints from: https://github.com/teamhide/fastapi-boilerplate/blob/master/core/db/session.py
db_session_context: ContextVar[Optional[int]] = ContextVar(
    "db_session_context", default=None
)


def get_db_session_context() -> int:
    session_id = db_session_context.get()

    if not session_id:
        raise ValueError("Currently no session is available")

    return session_id


def set_db_session_context(*, session_id: int) -> None:
    db_session_context.set(session_id)


# we don't need a separate engine for document DB(google firestore)
postgres_engine: AsyncEngine

if config.DB_TYPE == "postgres":
    postgres_engine = create_async_engine(url=config.DB_URL)

# session factories
_postgres_session_factory = async_scoped_session(
    session_factory=async_sessionmaker(
        bind=postgres_engine, autoflush=False, autocommit=False
    ),
    scopefunc=get_db_session_context,
)


def _firestore_session_factory() -> firestore.AsyncClient:
    return firestore.AsyncClient(
        project=gcp_infra_config.PROJECT_ID,
        credentials=gcp_infra_config.GOOGLE_APPLICATION_CREDENTIALS,
        database=gcp_infra_config.FIRESTORE_DB_NAME,
    )


_SessionFactoryType = (
    async_scoped_session[AsyncSession] | Callable[..., firestore.AsyncClient]
)
SessionType = AsyncSession | firestore.AsyncClient


@functools.cache
def _session_factory() -> _SessionFactoryType:
    session_factory: _SessionFactoryType

    if config.DB_TYPE == "postgres":
        session_factory = _postgres_session_factory

    else:  # config.DB_TYPE == "document"
        session_factory = _firestore_session_factory

    return session_factory


def get_current_session() -> SessionType:
    return _session_factory()
