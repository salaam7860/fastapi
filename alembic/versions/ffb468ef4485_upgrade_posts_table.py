"""upgrade posts table

Revision ID: ffb468ef4485
Revises: c2ecc39eecb8
Create Date: 2024-02-23 14:37:10.946741

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ffb468ef4485'
down_revision = 'c2ecc39eecb8'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True)
    , sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    # op.drop_table('posts')
    pass

