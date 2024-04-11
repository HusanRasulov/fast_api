"""auto-vote

Revision ID: 1cbcafab8f92
Revises: 3a3c59fc89fe
Create Date: 2024-04-10 16:01:52.552878

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '1cbcafab8f92'
down_revision: Union[str, None] = '3a3c59fc89fe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_primary_key('posts_pk', 'posts', ['id'])
    op.create_table(
        'votes',
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('post_id', sa.Integer, sa.ForeignKey('posts.id', ondelete='CASCADE'), primary_key=True)
    )


def downgrade() -> None:
    op.drop_table('votes')
