from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from ._session import get_current_session


CurrentDBSessionDependency = Annotated[AsyncSession, Depends(get_current_session)]
