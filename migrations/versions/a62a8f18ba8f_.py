"""empty message

Revision ID: a62a8f18ba8f
Revises: e91819f10f03
Create Date: 2019-05-22 10:00:26.063023

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a62a8f18ba8f'
down_revision = 'e91819f10f03'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('army', sa.Column('join_type', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('army', 'join_type')
    # ### end Alembic commands ###