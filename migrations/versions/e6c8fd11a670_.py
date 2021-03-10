"""empty message

Revision ID: e6c8fd11a670
Revises: 7861cbc4ab13
Create Date: 2021-03-11 06:58:41.358845

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e6c8fd11a670'
down_revision = '7861cbc4ab13'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('meal',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('model')
    op.drop_table('cars')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cars',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('model', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('doors', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='cars_pkey')
    )
    op.create_table('model',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('model', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('doors', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='model_pkey')
    )
    op.drop_table('meal')
    # ### end Alembic commands ###
