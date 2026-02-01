"""rename user table to users

Revision ID: 8edc24c65b85
Revises: 67759fdd5c03
Create Date: 2026-01-31 06:42:47.886387

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8edc24c65b85'
down_revision = '67759fdd5c03'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.rename_table("user", "users")


def downgrade() -> None:
    op.rename_table("users", "user")
