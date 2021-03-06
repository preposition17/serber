"""empty message

Revision ID: b0df6cd8e413
Revises: e1faef576bda
Create Date: 2022-01-31 00:50:29.702454

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'b0df6cd8e413'
down_revision = 'e1faef576bda'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('wax_account', sa.Column('atomic_drop_balance', sa.Float(), nullable=True))
    op.add_column('wax_account', sa.Column('nefty_drop_balance', sa.Float(), nullable=True))
    op.drop_column('wax_account', 'drop_balance')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('wax_account', sa.Column('drop_balance', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.drop_column('wax_account', 'nefty_drop_balance')
    op.drop_column('wax_account', 'atomic_drop_balance')
    # ### end Alembic commands ###
