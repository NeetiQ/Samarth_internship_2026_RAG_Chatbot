"""Add user_id ownership and is_shared to documents and chat_sessions

Revision ID: a1b2c3d4e5f6
Revises: 42c012d1e796
Create Date: 2026-07-01 14:40:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, None] = '42c012d1e796'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # --- documents: add user_id FK and is_shared flag ---
    op.add_column('documents', sa.Column('user_id', sa.Integer(), nullable=True))
    op.add_column('documents', sa.Column('is_shared', sa.Boolean(), nullable=False, server_default=sa.text('false')))
    op.create_index('ix_documents_user_id', 'documents', ['user_id'], unique=False)
    op.create_foreign_key(
        'fk_documents_user_id_app_users',
        'documents', 'app_users',
        ['user_id'], ['id'],
        ondelete='CASCADE'
    )

    # --- chat_sessions: add user_id FK ---
    op.add_column('chat_sessions', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_index('ix_chat_sessions_user_id', 'chat_sessions', ['user_id'], unique=False)
    op.create_foreign_key(
        'fk_chat_sessions_user_id_app_users',
        'chat_sessions', 'app_users',
        ['user_id'], ['id'],
        ondelete='CASCADE'
    )

    # --- Mark all existing documents as shared (system-owned legacy data) ---
    op.execute("UPDATE documents SET is_shared = true WHERE user_id IS NULL")

    # --- Make hashed_password NOT NULL on app_users ---
    # First set any existing NULL values to a placeholder (won't be valid bcrypt)
    op.execute("UPDATE app_users SET hashed_password = 'PLACEHOLDER_NEEDS_RESET' WHERE hashed_password IS NULL")
    op.alter_column('app_users', 'hashed_password', nullable=False)


def downgrade() -> None:
    # --- Revert app_users ---
    op.alter_column('app_users', 'hashed_password', nullable=True)

    # --- Revert chat_sessions ---
    op.drop_constraint('fk_chat_sessions_user_id_app_users', 'chat_sessions', type_='foreignkey')
    op.drop_index('ix_chat_sessions_user_id', table_name='chat_sessions')
    op.drop_column('chat_sessions', 'user_id')

    # --- Revert documents ---
    op.drop_constraint('fk_documents_user_id_app_users', 'documents', type_='foreignkey')
    op.drop_index('ix_documents_user_id', table_name='documents')
    op.drop_column('documents', 'is_shared')
    op.drop_column('documents', 'user_id')
