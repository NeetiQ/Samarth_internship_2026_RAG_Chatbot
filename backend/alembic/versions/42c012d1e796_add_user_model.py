"""Add User model

Revision ID: 42c012d1e796
Revises: 577976d46e58
Create Date: 2026-07-01 11:01:59.703480

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '42c012d1e796'
down_revision: Union[str, None] = '577976d46e58'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'app_users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=True),
        sa.Column('full_name', sa.String(length=255), nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default=sa.text('true'), nullable=True),
        sa.Column('is_superuser', sa.Boolean(), server_default=sa.text('false'), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_app_users')),
    )
    op.create_index(op.f('ix_app_users_email'), 'app_users', ['email'], unique=True)
    op.create_index(op.f('ix_app_users_id'), 'app_users', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_app_users_id'), table_name='app_users')
    op.drop_index(op.f('ix_app_users_email'), table_name='app_users')
    op.drop_table('app_users')
