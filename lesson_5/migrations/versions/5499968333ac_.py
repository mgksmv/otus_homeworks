"""empty message

Revision ID: 5499968333ac
Revises: 
Create Date: 2022-05-28 18:21:45.063933

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5499968333ac'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.Column('color', sa.String(length=6), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=32), nullable=False),
    sa.Column('first_name', sa.String(length=32), nullable=True),
    sa.Column('last_name', sa.String(length=32), nullable=True),
    sa.Column('bio', sa.String(length=255), nullable=True),
    sa.Column('email', sa.String(length=32), nullable=False),
    sa.Column('password', sa.String(length=100), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('blogs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('blog_tags',
    sa.Column('blog_id', sa.Integer(), nullable=True),
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['blog_id'], ['blogs.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ondelete='SET NULL')
    )
    op.create_table('bookmarks',
    sa.Column('blog_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['blog_id'], ['blogs.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(length=255), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('blog_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['blog_id'], ['blogs.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comments')
    op.drop_table('bookmarks')
    op.drop_table('blog_tags')
    op.drop_table('blogs')
    op.drop_table('users')
    op.drop_table('tags')
    # ### end Alembic commands ###