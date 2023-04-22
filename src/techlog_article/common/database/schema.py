from typing import Optional
from datetime import datetime
from uuid import UUID

from sqlalchemy import String, ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    # default fields for every orm object
    created_at: Mapped[datetime] = mapped_column(server_defuault=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(default=None)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(default=None)


class DBUser(Base):
    __tablename__ = "user"

    # fields
    id: Mapped[UUID] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(index=True)

    # relationship
    auth: Mapped["DBAuth"] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"DBUser id={self.id!r}"


class DBAuth(Base):
    """
    Remark: since you can't directly store a UUID data into a MySQL database,
    you have to convert it to other data formats
    """

    __tablename__ = "auth"

    # fields
    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("user.id"))
    access_token: Mapped[str] = mapped_column(String(255), default="")

    # relationship
    user: Mapped[DBUser] = relationship(back_populates="auth")

    def __repr__(self) -> str:
        return f"DBAuth id={self.id!r}"
