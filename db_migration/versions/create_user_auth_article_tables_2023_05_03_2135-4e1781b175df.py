"""create user auth article tables

Revision ID: 4e1781b175df
Revises: cc40bcb48d81
Create Date: 2023-05-03 21:35:31.981605

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "4e1781b175df"
down_revision = "cc40bcb48d81"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("id", sa.UUID, primary_key=True),
        sa.Column("username", sa.String(16), index=True),
        sa.Column("email", sa.String, index=True),
        sa.Column("hashed_password", sa.String),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, default=None, onupdate=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime, nullable=True),
    )

    op.create_table(
        "auth",
        sa.Column("id", sa.UUID, primary_key=True),
        sa.Column("user_id", sa.UUID, sa.ForeignKey("user.id"), index=True),
        sa.Column("access_token", sa.String, nullable=True),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, default=None, onupdate=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime, nullable=True),
    )

    op.create_table(
        "article",
        sa.Column("id", sa.UUID, primary_key=True),
        sa.Column("author_id", sa.UUID, sa.ForeignKey("user.id"), index=True),
        sa.Column("title", sa.String(32)),
        sa.Column("content", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, default=None, onupdate=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime, nullable=True),
    )


def downgrade() -> None:
    op.drop_table("auth")
    op.drop_table("article")
    op.drop_table("user")
