"""Change precision and scale of numeric value

Revision ID: c9d64e4d9976
Revises: f2bf141c6f3a
Create Date: 2022-06-28 18:41:45.719656

"""
import sqlalchemy as sa
from pydantic import NumberNotGeError

from alembic import op

# revision identifiers, used by Alembic.
revision = "c9d64e4d9976"
down_revision = "f2bf141c6f3a"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "accounts",
        "dust_dollars",
        existing_type=sa.NUMERIC(precision=2),
        type_=sa.NUMERIC(precision=9, scale=2),
    )


# ### end Alembic commands ###


def downgrade():
    op.alter_column(
        "accounts",
        "dust_dollars",
        type_=sa.NUMERIC(precision=2),
        existing_type=sa.NUMERIC(precision=9, scale=2),
    )
