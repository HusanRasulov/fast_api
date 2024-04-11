"""add foreign key to the post table

Revision ID: 3757ec282f85
Revises: bf673a52afbf
Create Date: 2024-04-10 14:48:39.281536

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '3757ec282f85'
down_revision: Union[str, None] = 'bf673a52afbf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'posts',
        sa.Column('user_id', sa.Integer, nullable=False)
    )
    pass


def downgrade() -> None:
    op.drop_constraint("post_users_fk", 'posts')
    op.drop_column('posts', 'user_id')
    pass
