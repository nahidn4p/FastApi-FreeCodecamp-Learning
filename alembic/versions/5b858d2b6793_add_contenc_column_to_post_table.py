"""Add contenc column to  post table

Revision ID: 5b858d2b6793
Revises: d1d4858849d6
Create Date: 2024-11-21 12:58:50.302770

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5b858d2b6793'
down_revision: Union[str, None] = 'd1d4858849d6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'posts',
        sa.Column('content', sa.String(), nullable=False)
    )

    pass


def downgrade() -> None:
    op.drop_column('posts', 'contents')
    pass
