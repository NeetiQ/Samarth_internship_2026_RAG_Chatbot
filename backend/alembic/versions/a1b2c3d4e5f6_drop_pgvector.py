"""drop pgvector

Revision ID: a1b2c3d4e5f6
Revises: 577976d46e58
Create Date: 2026-07-03 23:36:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
# In a downgrade we might need pgvector but since we are removing the dependency entirely,
# keeping pgvector in downgrade might cause issues if pgvector library is absent.
# However, Alembic usually relies on the models or raw SQL. We will use raw SQL for downgrade if needed, or just type it safely.
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, None] = '577976d46e58'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Drop embedding column
    op.drop_column('legal_chunks', 'embedding')
    # Drop vector extension
    op.execute('DROP EXTENSION IF EXISTS vector;')

def downgrade() -> None:
    # Re-create vector extension
    op.execute('CREATE EXTENSION IF NOT EXISTS vector;')
    # We can't import pgvector if it's removed from requirements, so we use raw text type
    op.add_column('legal_chunks', sa.Column('embedding', postgresql.ARRAY(sa.Float()), nullable=True))
    op.execute('ALTER TABLE legal_chunks ALTER COLUMN embedding TYPE vector(384) USING embedding::vector;')
