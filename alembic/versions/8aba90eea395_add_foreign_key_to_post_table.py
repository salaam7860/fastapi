"""add foreign key to post table

Revision ID: 8aba90eea395
Revises: 2b299b805142
Create Date: 2024-02-23 15:15:41.188088

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8aba90eea395'
down_revision = '2b299b805142'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
