"""add thumbnail_url column to article table

Revision ID: 7e5bd7671bb6
Revises: 4e1781b175df
Create Date: 2024-02-10 12:38:14.921540

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "7e5bd7671bb6"
down_revision = "4e1781b175df"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("article", sa.Column("thumbnail_url", sa.Text, nullable=True))


def downgrade() -> None:
    op.drop_column("article", "thumbnail_url")
