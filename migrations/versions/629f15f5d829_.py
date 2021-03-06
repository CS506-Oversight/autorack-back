"""empty message

Revision ID: 629f15f5d829
Revises: 298275443219
Create Date: 2021-04-26 22:09:59.768473

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '629f15f5d829'
down_revision = '298275443219'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('order',
    sa.Column('order_id', sa.String(), nullable=False),
    sa.Column('user_id', sa.String(), nullable=False),
    sa.Column('order', sa.String(), nullable=True),
    sa.Column('date', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('order_id')
    )
    op.create_table('supplier',
    sa.Column('ingredient_id', sa.String(), nullable=False),
    sa.Column('ingredient_price', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.PrimaryKeyConstraint('ingredient_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('supplier')
    op.drop_table('order')
    # ### end Alembic commands ###
