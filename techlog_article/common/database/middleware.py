from typing import Callable, Awaitable

from fastapi import Request, Response, status as HTTPStatus

from ._session import get_session_manager

session_manager = get_session_manager()


async def db_session_middleware_function(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    response = Response(
        "Internal server error", status_code=HTTPStatus.HTTP_500_INTERNAL_SERVER_ERROR
    )

    try:
        session_manager.set_db_session_context(session_id=hash(request))
        response = await call_next(request)

    finally:
        await (
            session_manager.remove_current_session()
        )  # this includes closing the session as well
        session_manager.set_db_session_context(session_id=None)

    return response
