"""empty message

Revision ID: 180d24effd4a
Revises: 3fb4f0934000
Create Date: 2014-11-16 01:59:13.791752

"""

# revision identifiers, used by Alembic.
revision = '180d24effd4a'
down_revision = '3fb4f0934000'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ware_house',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=True),
    sa.Column('address', sa.String(length=250), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('good',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('count', sa.Integer(), nullable=True),
    sa.Column('barcode', sa.BigInteger(), nullable=True),
    sa.Column('full_name', sa.String(length=250), nullable=True),
    sa.Column('commodity_id', sa.Integer(), nullable=True),
    sa.Column('price_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['commodity_id'], ['commodity.id'], ),
    sa.ForeignKeyConstraint(['price_id'], ['price.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('acceptance',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('invoice_id', sa.Integer(), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['invoice_id'], ['invoice.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('acceptance')
    op.drop_table('good')
    op.drop_table('ware_house')
    ### end Alembic commands ###
