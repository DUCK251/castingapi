"""empty message

Revision ID: 4a7dd499ce2d
Revises: 
Create Date: 2020-11-13 17:42:41.279920

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4a7dd499ce2d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('actors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('gender', sa.Enum('male', 'female', name='gender'), nullable=False),
    sa.Column('location', sa.String(), nullable=False),
    sa.Column('passport', sa.Boolean(), nullable=True),
    sa.Column('driver_license', sa.Boolean(), nullable=True),
    sa.Column('ethnicity', sa.Enum('asian', 'black', 'latino', 'middle eastern', 'south asian', 'southeast asian', 'white', name='ethnicity'), nullable=True),
    sa.Column('hair_color', sa.Enum('black', 'brown', 'blond', 'auburn', 'chestnut', 'red', 'gray', 'white', 'bald', name='hair_color'), nullable=True),
    sa.Column('eye_color', sa.Enum('amber', 'blue', 'brown', 'gray', 'green', 'hazel', 'red', 'violet', name='eye_color'), nullable=True),
    sa.Column('body_type', sa.Enum('average', 'slim', 'athletic', 'muscular', 'curvy', 'heavyset', 'plus-sized', name='body_type'), nullable=True),
    sa.Column('height', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('image_link', sa.String(), nullable=True),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('movies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('release_date', sa.Date(), nullable=False),
    sa.Column('company', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('movie_id', sa.Integer(), nullable=False),
    sa.Column('actor_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('gender', sa.Enum('male', 'female', name='gender'), nullable=False),
    sa.Column('min_age', sa.Integer(), nullable=False),
    sa.Column('max_age', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['actor_id'], ['actors.id'], ),
    sa.ForeignKeyConstraint(['movie_id'], ['movies.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('roles')
    op.drop_table('movies')
    op.drop_table('actors')
    # ### end Alembic commands ###
