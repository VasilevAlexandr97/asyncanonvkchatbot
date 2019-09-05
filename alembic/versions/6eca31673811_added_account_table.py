"""Added account table

Revision ID: 6eca31673811
Revises: ddeafdbe94e4
Create Date: 2019-09-04 19:11:04.125560

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6eca31673811'
down_revision = 'ddeafdbe94e4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rooms', sa.Column('reputation', sa.Float(), nullable=True))
    op.add_column('users', sa.Column('age', sa.String(length=8), nullable=True))
    op.add_column('users', sa.Column('find_sex', sa.String(length=8), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'find_sex')
    op.drop_column('users', 'age')
    op.drop_column('rooms', 'reputation')
    # ### end Alembic commands ###
