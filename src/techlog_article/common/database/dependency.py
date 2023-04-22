from fastapi import Request

from sqlalchemy.ext.asyncio import AsyncSession


def get_db_session(request: Request) -> AsyncSession:
    if not hasattr(request.state, "db_session") or not isinstance(
        request.state.db_session, AsyncSession
    ):
        raise AttributeError("DB session has not been provided")

    return request.state.db_session
