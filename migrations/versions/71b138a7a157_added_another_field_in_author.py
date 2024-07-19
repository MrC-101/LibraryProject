"""added another field in Author

Revision ID: 71b138a7a157
Revises: d54fb5b66e67
Create Date: 2024-07-19 05:07:06.690389

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '71b138a7a157'
down_revision = 'd54fb5b66e67'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('authors', schema=None) as batch_op:
        batch_op.add_column(sa.Column('died', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('authors', schema=None) as batch_op:
        batch_op.drop_column('died')

    # ### end Alembic commands ###
