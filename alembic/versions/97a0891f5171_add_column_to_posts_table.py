"""add column to posts table

Revision ID: 97a0891f5171
Revises: ffb468ef4485
Create Date: 2024-02-23 14:40:33.196566

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '97a0891f5171'
down_revision = 'ffb468ef4485'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
