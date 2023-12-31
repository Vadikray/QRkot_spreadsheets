"""Add full amount in CharityProject

Revision ID: 484255e78c7d
Revises: 50a1151dc0b4
Create Date: 2023-07-13 16:21:04.716749

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '484255e78c7d'
down_revision = '50a1151dc0b4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('charityproject', sa.Column('full_amount', sa.Integer(), nullable=False))
    op.add_column('charityproject', sa.Column('invested_amount', sa.Integer(), nullable=True))
    op.add_column('charityproject', sa.Column('fully_invested', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('charityproject', 'fully_invested')
    op.drop_column('charityproject', 'invested_amount')
    op.drop_column('charityproject', 'full_amount')
    # ### end Alembic commands ###
