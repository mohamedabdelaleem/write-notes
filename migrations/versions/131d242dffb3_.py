"""empty message

Revision ID: 131d242dffb3
Revises: 3ed43129821f
Create Date: 2020-04-25 02:09:57.907448

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '131d242dffb3'
down_revision = '3ed43129821f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('note', schema=None) as batch_op:
        batch_op.drop_column('num')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('note', schema=None) as batch_op:
        batch_op.add_column(sa.Column('num', sa.INTEGER(), nullable=True))

    # ### end Alembic commands ###
