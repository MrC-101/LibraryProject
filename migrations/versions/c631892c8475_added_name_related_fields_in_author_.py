"""added name related fields in Author model

Revision ID: c631892c8475
Revises: bf08f500f776
Create Date: 2024-07-22 04:32:22.934626

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c631892c8475'
down_revision = 'bf08f500f776'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('authors', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fname', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('lname', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('authors', schema=None) as batch_op:
        batch_op.drop_column('lname')
        batch_op.drop_column('fname')

    # ### end Alembic commands ###
