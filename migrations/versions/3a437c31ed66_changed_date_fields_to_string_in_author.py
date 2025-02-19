"""changed date fields to string in Author

Revision ID: 3a437c31ed66
Revises: 71b138a7a157
Create Date: 2024-07-19 15:02:58.893649

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3a437c31ed66'
down_revision = '71b138a7a157'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('authors', schema=None) as batch_op:
        batch_op.alter_column('born',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=4),
               existing_nullable=True)
        batch_op.alter_column('died',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=4),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('authors', schema=None) as batch_op:
        batch_op.alter_column('died',
               existing_type=sa.String(length=4),
               type_=sa.INTEGER(),
               existing_nullable=True)
        batch_op.alter_column('born',
               existing_type=sa.String(length=4),
               type_=sa.INTEGER(),
               existing_nullable=True)

    # ### end Alembic commands ###
