"""create_user_and_auth_tables

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
    )

    op.create_table(
        "auth",
        sa.Column("id", sa.UUID, primary_key=True),
        sa.Column("user_id", sa.UUID, sa.ForeignKey("user.id")),
        sa.Column("access_token", sa.String, nullable=True),
    )


def downgrade() -> None:
    op.drop_table("auth")
