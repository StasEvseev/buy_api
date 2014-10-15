"""empty message

Revision ID: 4f8d0321cbca
Revises: 3763273f85f5
Create Date: 2014-10-15 20:08:09.676245

"""

# revision identifiers, used by Alembic.
revision = '4f8d0321cbca'
down_revision = '3763273f85f5'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('invoice_item', sa.Column('number_global', sa.String(length=250), nullable=True))
    op.add_column('invoice_item', sa.Column('number_local', sa.String(length=250), nullable=True))
    op.drop_column('invoice_item', 'number')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('invoice_item', sa.Column('number', sa.VARCHAR(length=250), autoincrement=False, nullable=True))
    op.drop_column('invoice_item', 'number_local')
    op.drop_column('invoice_item', 'number_global')
    ### end Alembic commands ###
