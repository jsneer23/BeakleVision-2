"""add NOT_PLAYED to matchwinner enum

Revision ID: 40a632bde62b
Revises: c4e4b56e5ca1
Create Date: 2025-07-09 22:42:04.001586

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '40a632bde62b'
down_revision = 'c4e4b56e5ca1'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("ALTER TYPE matchwinner ADD VALUE 'NOT_PLAYED'")


def downgrade():
    pass
