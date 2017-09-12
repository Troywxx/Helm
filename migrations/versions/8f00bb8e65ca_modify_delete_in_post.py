"""modify delete in Post

Revision ID: 8f00bb8e65ca
Revises: fd97065a70bf
Create Date: 2017-07-26 11:10:58.184039

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f00bb8e65ca'
down_revision = 'fd97065a70bf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('deleted', sa.Boolean(), nullable=True))
    op.add_column('posts', sa.Column('modify_count', sa.Integer(), nullable=True))
    op.add_column('posts', sa.Column('show_ack', sa.Boolean(), nullable=True))
    op.create_index(op.f('ix_posts_deleted'), 'posts', ['deleted'], unique=False)
    op.create_index(op.f('ix_posts_show_ack'), 'posts', ['show_ack'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_posts_show_ack'), table_name='posts')
    op.drop_index(op.f('ix_posts_deleted'), table_name='posts')
    op.drop_column('posts', 'show_ack')
    op.drop_column('posts', 'modify_count')
    op.drop_column('posts', 'deleted')
    # ### end Alembic commands ###