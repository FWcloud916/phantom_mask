"""create pharmacies table

Revision ID: a91ccebefdd1
Revises: 53298d7d7a83
Create Date: 2022-11-11 00:47:09.001643

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Computed
from sqlalchemy_utils import TSVectorType

# revision identifiers, used by Alembic.
revision = 'a91ccebefdd1'
down_revision = '53298d7d7a83'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'pharmacies',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('name', sa.String, index=True),
        sa.Column('name_tsv', TSVectorType('name'),
                  Computed("to_tsvector('simple', \"name\")", persisted=True)),
        sa.Column('cash_balance', sa.Float, default=0),
        sa.Column('created_at', sa.DateTime, default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, default=sa.func.now(), onupdate=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('pharmacies')
