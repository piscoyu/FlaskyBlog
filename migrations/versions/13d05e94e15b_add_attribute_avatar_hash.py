"""add attribute avatar_hash

Revision ID: 13d05e94e15b
Revises: 2217a1c2c684
Create Date: 2016-05-09 23:48:31.155000

"""

# revision identifiers, used by Alembic.
revision = '13d05e94e15b'
down_revision = '2217a1c2c684'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('avatar_hash', sa.String(length=32), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'avatar_hash')
    ### end Alembic commands ###
