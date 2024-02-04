from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from ._session import get_session_manager

session_manager = get_session_manager()

CurrentDBSessionDependency = Annotated[
    AsyncSession, Depends(session_manager.get_current_session)
]
