"""changed fullname

Revision ID: 3ad0a81046f9
Revises: 99fa7ed98a37
Create Date: 2024-07-18 03:42:52.577847

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ad0a81046f9'
down_revision = '99fa7ed98a37'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('authors', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fullname', sa.String(), nullable=False))
        batch_op.drop_column('fname')
        batch_op.drop_column('lname')

    with op.batch_alter_table('book_author', schema=None) as batch_op:
        batch_op.alter_column('book_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('author_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book_author', schema=None) as batch_op:
        batch_op.alter_column('author_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('book_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    with op.batch_alter_table('authors', schema=None) as batch_op:
        batch_op.add_column(sa.Column('lname', sa.VARCHAR(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('fname', sa.VARCHAR(), autoincrement=False, nullable=False))
        batch_op.drop_column('fullname')

    # ### end Alembic commands ###
