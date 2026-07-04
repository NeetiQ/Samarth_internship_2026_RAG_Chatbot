"""Merge drop pgvector and add auth ownership

Revision ID: 7890b6f78023
Revises: a1b2c3d4e5f6, b2c3d4e5f6a1
Create Date: 2026-07-04 14:32:32.607852

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7890b6f78023'
down_revision: Union[str, None] = ('a1b2c3d4e5f6', 'b2c3d4e5f6a1')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    pass

def downgrade() -> None:
    pass
