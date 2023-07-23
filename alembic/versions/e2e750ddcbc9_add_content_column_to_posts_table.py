"""add content column to posts table

Revision ID: e2e750ddcbc9
Revises: b8ae9a96eb07
Create Date: 2023-07-23 15:35:35.823573

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2e750ddcbc9'
down_revision = 'b8ae9a96eb07'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
