"""added some more columns to Publisher table

Revision ID: 57a0d76bb69b
Revises: fa6ccc3333e1
Create Date: 2024-07-31 16:48:57.357903

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57a0d76bb69b'
down_revision = 'fa6ccc3333e1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('publishers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('publ_founder', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('publ_parent', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('publ_website', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('publishers', schema=None) as batch_op:
        batch_op.drop_column('publ_website')
        batch_op.drop_column('publ_parent')
        batch_op.drop_column('publ_founder')

    # ### end Alembic commands ###
