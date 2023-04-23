from typing import Callable, Awaitable, Optional, Annotated
from contextvars import ContextVar

from fastapi import Request, Response, status as HTTPStatus, Depends
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_scoped_session,
    async_sessionmaker,
    AsyncSession,
)

from ..config import config

# some hints from: https://github.com/teamhide/fastapi-boilerplate/blob/master/core/db/session.py
db_session_context: ContextVar[Optional[int]] = ContextVar(
    "db_session_context", default=None
)
engine = create_async_engine(url=config.DB_URL)


def get_db_session_context() -> int:
    session_id = db_session_context.get()

    if not session_id:
        raise ValueError("Currently no session is available")

    return session_id


def set_db_session_context(*, session_id: int) -> None:
    db_session_context.set(session_id)


AsyncScopedSession = async_scoped_session(
    session_factory=async_sessionmaker(bind=engine, autoflush=False, autocommit=False),
    scopefunc=get_db_session_context,
)


def get_current_session() -> AsyncSession:
    return AsyncScopedSession()


CurrentDBSessionDependency = Annotated[AsyncSession, Depends(get_current_session)]


async def db_session_middleware(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    response = Response(
        "Internal server error", status_code=HTTPStatus.HTTP_500_INTERNAL_SERVER_ERROR
    )

    try:
        set_db_session_context(hash(request))
        request.state.db_session = AsyncScopedSession()
        response = await call_next(request)

    finally:
        await AsyncScopedSession.remove()
        set_db_session_context(None)

    return response
