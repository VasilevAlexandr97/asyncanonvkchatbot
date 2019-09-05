"""Added account table

Revision ID: 450434548e46
Revises: 641a1b0151da
Create Date: 2019-09-04 17:18:25.297780

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '450434548e46'
down_revision = '641a1b0151da'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rooms',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('f_user', sa.Integer(), nullable=False),
    sa.Column('s_user', sa.Integer(), nullable=False),
    sa.Column('first_message_time', sa.DateTime(), nullable=True),
    sa.Column('last_message_time', sa.DateTime(), nullable=True),
    sa.Column('sex', sa.String(length=8), nullable=True),
    sa.Column('find_sex', sa.String(length=8), nullable=True),
    sa.Column('find_age', sa.String(length=8), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('users', sa.Column('room', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('sex', sa.String(length=8), nullable=False))
    op.add_column('users', sa.Column('state', sa.String(length=32), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'state')
    op.drop_column('users', 'sex')
    op.drop_column('users', 'room')
    op.drop_table('rooms')
    # ### end Alembic commands ###
