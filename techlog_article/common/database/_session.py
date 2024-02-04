from __future__ import annotations

from typing import Optional, cast
from contextvars import ContextVar
import functools

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_scoped_session,
    async_sessionmaker,
    AsyncSession,
)

from google.cloud import firestore
from ._firestore import FirestoreSessionFactory

from ..config import config, gcp_infra_config

SessionType = AsyncSession | firestore.AsyncClient


def make_session_manager() -> _SessionContextManager:
    # session context manager
    session_context_manager = _SessionContextManager()

    # session factories
    if config.DB_TYPE == "postgres":
        postgres_engine = create_async_engine(url=config.DB_URL)

        # AsyncScopedSession(in the official docs)
        session_factory = async_scoped_session(
            session_factory=async_sessionmaker(
                bind=postgres_engine, autoflush=False, autocommit=False
            ),
            scopefunc=session_context_manager.get_db_session_context,
        )

    else:  # config.DB_TYPE = "firestore"
        session_factory = FirestoreSessionFactory(
            session_cache=dict(),
            session_context_getter=session_context_manager.get_db_session_context,
            gcp_project_id=gcp_infra_config.PROJECT_ID,
            gcp_credentials_path=gcp_infra_config.GOOGLE_APPLICATION_CREDENTIALS,
            database_name=gcp_infra_config.FIRESTORE_DB_NAME,
        )

    return _SessionManager(
        session_context_manager=session_context_manager, session_factory=session_factory
    )


@functools.cache
def get_session_manager() -> _SessionManager:
    return make_session_manager()


class _SessionContextManager:
    """
    Manages global session contexts for concurrent requests
    """

    def __init__(self):
        self._db_session_context: ContextVar[Optional[int]] = ContextVar(
            "db_session_context", default=None
        )

    def get_db_session_context(self) -> int:
        session_id = self._db_session_context.get()

        if not session_id:
            raise ValueError("Currently no session is available")

        return session_id

    def set_db_session_context(self, *, session_id: int) -> None:
        self._db_session_context.set(session_id)


class _SessionManager:
    """
    Manages various DB sessions with only exposing abstracted interface

    referemce: https://github.com/teamhide/fastapi-boilerplate/blob/master/core/db/session.py
    """

    def __init__(
        self,
        *,
        session_context_manager: _SessionContextManager,
        session_factory: async_scoped_session[AsyncSession] | FirestoreSessionFactory,
    ):
        self._session_context_manager = session_context_manager
        self._session_factory = session_factory

    def get_db_session_context(self) -> int:
        return self._session_context_manager.get_db_session_context()

    def set_db_session_context(self, *, session_id: int) -> None:
        return self._session_context_manager.set_db_session_context(session_id)

    def get_current_session(self) -> SessionType:
        return self._session_factory()

    async def remove_current_session(self) -> None:
        if config.DB_TYPE == "postgres":
            await cast(
                async_scoped_session[AsyncSession], self._session_factory
            ).remove()

        elif config.DB_TYPE == "firestore":
            cast(
                FirestoreSessionFactory, self._session_factory
            ).remove_current_session()
