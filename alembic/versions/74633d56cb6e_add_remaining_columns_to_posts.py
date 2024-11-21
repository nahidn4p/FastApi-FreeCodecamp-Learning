"""Add Remaining Columns to posts

Revision ID: 74633d56cb6e
Revises: 300f953606fa
Create Date: 2024-11-21 13:23:34.542852

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '74633d56cb6e'
down_revision: Union[str, None] = '300f953606fa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',
                  sa.Column('published', sa.Boolean(),nullable=False, server_default='True'))
    op.add_column('posts',
                  sa.Column('created_at', sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('NOW()'))
                  )
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
