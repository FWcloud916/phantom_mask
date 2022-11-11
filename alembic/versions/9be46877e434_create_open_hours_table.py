"""create open_hours table

Revision ID: 9be46877e434
Revises: a91ccebefdd1
Create Date: 2022-11-11 00:47:21.769603

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9be46877e434'
down_revision = 'a91ccebefdd1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'open_hours',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('pharmacy_id', sa.Integer, sa.ForeignKey('pharmacies.id')),
        sa.Column('day', sa.Integer),
        sa.Column('open_time', sa.String),
        sa.Column('close_time', sa.String),
        sa.Column('created_at', sa.DateTime, default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, default=sa.func.now(), onupdate=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_constraint('open_hours_pharmacy_id_fkey', 'open_hours', type_='foreignkey')
    op.drop_table('open_hours')
    pass
