"""empty message

Revision ID: e5d8b22056a
Revises: 41124ac6e47e
Create Date: 2014-12-04 18:00:06.749852

"""

# revision identifiers, used by Alembic.
revision = 'e5d8b22056a'
down_revision = '41124ac6e47e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sync',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date_start', sa.DateTime(), nullable=True),
    sa.Column('date_end', sa.DateTime(), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sync')
    ### end Alembic commands ###
