"""create_user_and_auth_and_article_tables

Revision ID: e2acdb9df438
Revises: cc40bcb48d81
Create Date: 2023-04-22 15:56:09.941818

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e2acdb9df438"
down_revision = "cc40bcb48d81"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # TODO: add this structure
    op.create_table(
        "user",
        sa.Column("id", sa.UUID, primary_key=True),
        sa.Column("username", sa.String(16), index=True),
        sa.Column("email", sa.String, index=True),
        sa.Column("hashed_password", sa.String),
    )

    op.create_table(
        "auth",
        sa.Column("id", sa.UUID, primary_key=True),
        sa.Column("user_id", sa.UUID, sa.ForeignKey("user.id"), index=True),
        sa.Column("access_token", sa.String, nullable=True),
    )

    op.create_table(
        "article",
        sa.Column("id", sa.UUID, primary_key=True),
        sa.Column("author_id", sa.UUID, sa.ForeignKey("user.id"), index=True),
        sa.Column("title", sa.String(32)),
        sa.Column("content", sa.Text, nullable=True),
    )


def downgrade() -> None:
    op.drop_table("user")
    op.drop_table("auth")
    op.drop_table("article")
