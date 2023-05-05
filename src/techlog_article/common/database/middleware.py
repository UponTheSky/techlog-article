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
        set_db_session_context(session_id=hash(request))
        response = await call_next(request)

    finally:
        await AsyncScopedSession.remove()  # this includes closing the session as well
        set_db_session_context(session_id=None)

    return response
