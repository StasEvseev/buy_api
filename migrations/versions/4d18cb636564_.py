"""empty message

Revision ID: 4d18cb636564
Revises: 2067dce9ed01
Create Date: 2014-12-11 13:35:09.584085

"""

# revision identifiers, used by Alembic.
from sqlalchemy.dialects.sqlite.pysqlite import SQLiteDialect_pysqlite

revision = '4d18cb636564'
down_revision = '2067dce9ed01'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    bind = op.get_bind()
    if type(bind.dialect) == SQLiteDialect_pysqlite:
        try:
            op.create_unique_constraint(None, 'acceptance', ['invoice_id'])
            op.create_unique_constraint(None, 'acceptance', ['waybill_id'])
        except Exception as exc:
            pass
    else:
        op.create_unique_constraint(None, 'acceptance', ['invoice_id'])
        op.create_unique_constraint(None, 'acceptance', ['waybill_id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'acceptance')
    op.drop_constraint(None, 'acceptance')
    ### end Alembic commands ###
