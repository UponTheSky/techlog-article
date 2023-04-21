from typing import final, Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from common.database import models


@final
class AuthRepository:
    def __init__(self, db_session: Session):
        self._db_session = db_session

    def read_by_user_id(self, user_id: str) -> models.Auth:
        stmt = select(models.Auth).where(models.Auth.user_id == user_id)
        return self._db_session.scalars(stmt).one_or_none()

    def update(self, *, orm: models.Auth, dao: dict[str, Any]) -> models.Auth:
        for field, value in dao:
            setattr(orm, field, value)

        self._db_session.flush(orm)
