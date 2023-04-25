from typing import Optional
from datetime import datetime
from uuid import UUID

from sqlalchemy import String, ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    # default fields for every orm object
    created_at: Mapped[datetime] = mapped_column(server_defuault=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        default=None, onupdate=func.now()
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(default=None)


class User(Base):
    __tablename__ = "user"

    # fields
    id: Mapped[UUID] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(16), index=True)
    email: Mapped[str] = mapped_column(index=True)
    hashed_password: Mapped[str] = mapped_column()

    # relationship
    auth: Mapped["Auth"] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"DB User id={self.id!r}"


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
        return f"DB Auth id={self.id!r}"
