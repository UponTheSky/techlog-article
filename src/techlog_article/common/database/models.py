from typing import Optional
from datetime import datetime
from uuid import UUID

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    # default fields for every orm object
    created_at: Mapped[datetime]
    updated_at: Mapped[Optional[datetime]] = mapped_column(default=None)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(default=None)


class User(Base):
    __tablename__ = "user"

    # fields
    # TODO: add index=True attribute when necessary
    id: Mapped[UUID] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(16), unique=True)

    # relationship
    auth: Mapped["Auth"] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"DBUser id={self.id!r}"


class Auth(Base):
    """
    Remark: since you can't directly store a UUID data into a MySQL database,
    you have to convert it to other data formats
    """

    __tablename__ = "auth"

    # fields
    id: Mapped[UUID] = mapped_column(primary_key=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"))
    access_token: Mapped[Optional[str]] = mapped_column(String(255))

    # relationship
    user: Mapped[User] = relationship(back_populates="auth")

    def __repr__(self) -> str:
        return f"DBAuth id={self.id!r}"
