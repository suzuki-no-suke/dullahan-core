"""add chatlog created_at/updated_at column

Revision ID: c0ed2ef7f73c
Revises: 71b7f9950c96
Create Date: 2025-04-30 06:35:23.452406

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c0ed2ef7f73c'
down_revision: Union[str, None] = '71b7f9950c96'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('chat_log', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True))
    op.add_column('chat_log', sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('chat_log', 'updated_at')
    op.drop_column('chat_log', 'created_at')
