"""add extra columns to posts table

Revision ID: 3a3c59fc89fe
Revises: 7b0720a4e7df
Create Date: 2024-04-10 15:44:32.767626

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '3a3c59fc89fe'
down_revision: Union[str, None] = '7b0720a4e7df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('is_published', sa.Boolean(), server_default='True'))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'is_published')
    pass
