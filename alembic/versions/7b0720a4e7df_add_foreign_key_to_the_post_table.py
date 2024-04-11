"""add foreign key to the post table

Revision ID: 7b0720a4e7df
Revises: 3757ec282f85
Create Date: 2024-04-10 15:39:52.910969

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7b0720a4e7df'
down_revision: Union[str, None] = '3757ec282f85'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_foreign_key(
        'posts_users_fk',
        source_table="posts",
        referent_table="users",
        local_cols=['user_id'],
        remote_cols=['id'],
        ondelete="CASCADE"
    )
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', 'posts')
    pass
