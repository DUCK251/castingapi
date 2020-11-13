"""empty message

Revision ID: 1e212d6dfddf
Revises: 6958ee2fa5c1
Create Date: 2020-11-04 21:47:38.541803

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1e212d6dfddf'
down_revision = '6958ee2fa5c1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('actors', 'gender')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('actors', sa.Column('gender', sa.BOOLEAN(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
