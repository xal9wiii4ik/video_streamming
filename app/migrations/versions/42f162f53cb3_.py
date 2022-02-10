"""empty message

Revision ID: 42f162f53cb3
Revises: 0c40b21429bd
Create Date: 2022-02-09 20:14:27.940369

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '42f162f53cb3'
down_revision = '0c40b21429bd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('video', 'title',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
    op.alter_column('video', 'description',
               existing_type=sa.VARCHAR(length=1020),
               nullable=False)
    op.alter_column('video', 'bucket_path',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('video', 'bucket_path',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
    op.alter_column('video', 'description',
               existing_type=sa.VARCHAR(length=1020),
               nullable=True)
    op.alter_column('video', 'title',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
    # ### end Alembic commands ###
