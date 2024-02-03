from typing import Optional
from datetime import datetime
from uuid import UUID

from sqlalchemy import String, Text, ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class TimestampMixin:
    # default fields for every orm object
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        default=None, onupdate=func.now()
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(default=None)


class Base(DeclarativeBase):
    """
    If we want the datetime type to have timezone, then we should specify
    a custom mapping as below.

    type_annotation_map = {
        datetime: TIMESTAMP(timezone=True),
    }

    For details, see: https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html
    """

    pass


class User(TimestampMixin, Base):
    __tablename__ = "user"

    # fields
    id: Mapped[UUID] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(16), index=True)
    email: Mapped[str] = mapped_column(index=True)
    hashed_password: Mapped[str] = mapped_column()

    # relationship
    auth: Mapped["Auth"] = relationship(back_populates="user")
    articles: Mapped[list["Article"]] = relationship(back_populates="author")

    def __repr__(self) -> str:
        return f"DB User id={self.id!r}"


class Auth(TimestampMixin, Base):
    """
    Remark: since you can't directly store a UUID data into a MySQL database,
    you have to convert it to other data formats
    """

    __tablename__ = "auth"

    # fields
    id: Mapped[UUID] = mapped_column(primary_key=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"), index=True)
    access_token: Mapped[Optional[str]] = mapped_column(String(255))

    # relationship
    user: Mapped[User] = relationship(back_populates="auth")

    def __repr__(self) -> str:
        return f"DB Auth id={self.id!r}"


class Article(TimestampMixin, Base):
    __tablename__ = "article"

    # fields
    id: Mapped[UUID] = mapped_column(primary_key=True)
    author_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"), index=True)
    title: Mapped[str] = mapped_column(String(32))
    content: Mapped[Optional[str]] = mapped_column(Text)

    # relatioship
    author: Mapped[User] = relationship(back_populates="articles")

    def __repr__(self) -> str:
        return f"DB Article id={self.id!r}"
