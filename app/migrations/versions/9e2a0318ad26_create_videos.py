"""create videos

Revision ID: 9e2a0318ad26
Revises: bde1aa0ecc9c
Create Date: 2022-01-11 16:13:19.167674

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e2a0318ad26'
down_revision = 'bde1aa0ecc9c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('account')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('account',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('username', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('password', sa.VARCHAR(length=500), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('first_name', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('last_name', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('is_staff', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='account_pkey'),
    sa.UniqueConstraint('username', name='account_username_key')
    )
    # ### end Alembic commands ###
