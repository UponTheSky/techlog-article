from typing import Callable, Awaitable, Optional
from contextvars import ContextVar

from fastapi import Request, Response, status as HTTPStatus
from sqlalchemy.ext.asyncio import AsyncSession

from ._session import AsyncScopedSession

db_session_context: ContextVar[Optional[AsyncSession]] = ContextVar(
    "db_session_context", default=None
)


async def db_session_middleware(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    response = Response(
        "Internal server error", status_code=HTTPStatus.HTTP_500_INTERNAL_SERVER_ERROR
    )

    try:
        request.state.db_session = AsyncScopedSession()
        response = await call_next(request)

    finally:
        request.state.db_session.close()

    return response
