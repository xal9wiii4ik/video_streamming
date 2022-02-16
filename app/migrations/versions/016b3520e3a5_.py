"""empty message

Revision ID: 016b3520e3a5
Revises: 9247c9d246df
Create Date: 2022-01-23 20:04:27.896499

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '016b3520e3a5'
down_revision = '9247c9d246df'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('video', sa.Column('upload_date', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('video', 'upload_date')
    # ### end Alembic commands ###
