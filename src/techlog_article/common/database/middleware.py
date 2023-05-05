from typing import Callable, Awaitable

from fastapi import Request, Response, status as HTTPStatus

from ._session import set_db_session_context, AsyncScopedSession


async def db_session_middleware_function(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    response = Response(
        "Internal server error", status_code=HTTPStatus.HTTP_500_INTERNAL_SERVER_ERROR
    )

    try:
        set_db_session_context(hash(request))
        response = await call_next(request)

    finally:
        await AsyncScopedSession.remove()
        set_db_session_context(None)

    return response
