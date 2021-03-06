"""create video and account table

Revision ID: 5449e1df21c0
Revises: 
Create Date: 2022-02-24 16:32:05.696261

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5449e1df21c0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('account', 'username',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
    op.alter_column('account', 'password',
               existing_type=sa.VARCHAR(length=500),
               nullable=False)
    op.alter_column('account', 'email',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
    op.alter_column('account', 'first_name',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
    op.alter_column('account', 'last_name',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('account', 'last_name',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
    op.alter_column('account', 'first_name',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
    op.alter_column('account', 'email',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
    op.alter_column('account', 'password',
               existing_type=sa.VARCHAR(length=500),
               nullable=True)
    op.alter_column('account', 'username',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
    # ### end Alembic commands ###
