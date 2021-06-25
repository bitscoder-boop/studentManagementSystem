"""empty message

Revision ID: 57f7604d0c8c
Revises: 7afd45f040cd
Create Date: 2021-06-19 14:52:40.472997

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57f7604d0c8c'
down_revision = '7afd45f040cd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['contact'])
        batch_op.drop_column('address')
        batch_op.drop_column('email')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.VARCHAR(length=24), nullable=True))
        batch_op.add_column(sa.Column('address', sa.TEXT(length=100), nullable=True))
        batch_op.drop_constraint(None, type_='unique')

    # ### end Alembic commands ###