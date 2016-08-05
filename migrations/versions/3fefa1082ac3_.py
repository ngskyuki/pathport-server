"""empty message

Revision ID: 3fefa1082ac3
Revises: edc3aa18f8ff
Create Date: 2016-08-05 02:50:48.224590

"""

# revision identifiers, used by Alembic.
revision = '3fefa1082ac3'
down_revision = 'edc3aa18f8ff'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('googleplace',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('place_id', sa.String(), nullable=True),
    sa.Column('data', postgresql.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('googleplaceraw')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('googleplaceraw',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('place_id', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('data', postgresql.JSON(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='googleplaceraw_pkey')
    )
    op.drop_table('googleplace')
    ### end Alembic commands ###
