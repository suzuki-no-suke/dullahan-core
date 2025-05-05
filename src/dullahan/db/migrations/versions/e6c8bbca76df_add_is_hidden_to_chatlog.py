"""add_is_hidden_to_chatlog

Revision ID: e6c8bbca76df
Revises: c0ed2ef7f73c
Create Date: 2025-05-05 20:17:17.523864

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e6c8bbca76df'
down_revision: Union[str, None] = 'c0ed2ef7f73c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('chat_log', sa.Column('is_hidden', sa.Boolean(), nullable=False, server_default='false'))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('chat_log', 'is_hidden') 

