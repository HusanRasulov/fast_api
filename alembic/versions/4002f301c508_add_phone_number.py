"""add phone number

Revision ID: 4002f301c508
Revises: 1cbcafab8f92
Create Date: 2024-04-11 09:55:22.943148

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '4002f301c508'
down_revision: Union[str, None] = '1cbcafab8f92'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=False))
    op.create_unique_constraint(None, 'users', ['phone_number'])


def downgrade() -> None:
    op.drop_constraint('None', 'users')
    op.drop_column('users', 'phone_number')
