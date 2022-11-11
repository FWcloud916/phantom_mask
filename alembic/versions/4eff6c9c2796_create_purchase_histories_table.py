"""create purchase_histories table

Revision ID: 4eff6c9c2796
Revises: 4272dc77222e
Create Date: 2022-11-11 05:27:35.950582

"""
from datetime import datetime

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4eff6c9c2796'
down_revision = '4272dc77222e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'purchase_histories',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('mask_name', sa.String, nullable=False),
        sa.Column('pharmacy_name', sa.String, nullable=False),
        sa.Column('transaction_amount', sa.Float, default=0),
        sa.Column('transaction_date', sa.DateTime, default=datetime.now),
    )


def downgrade() -> None:
    op.drop_constraint('purchase_histories_user_id_fkey', 'purchase_histories', type_='foreignkey')
    op.drop_table('purchase_histories')
    pass
