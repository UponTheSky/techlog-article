from typing import Optional, final

from sqlalchemy import select
from sqlalchemy.orm import Session

from common.database import models


@final
class UserRepository:
    def __init__(self, *, db_session: Session):
        self._db_session = db_session

    def read_by_username(self, username: str) -> Optional[models.User]:
        stmt = select(models.User).where(models.User.username == username)
        return self._db_session.scalars(stmt).one_or_none()

    def read_by_id(self, id: str) -> Optional[models.User]:
        stmt = select(models.User).where(models.User.id == id)
        return self._db_session.scalars(stmt).one_or_none()
