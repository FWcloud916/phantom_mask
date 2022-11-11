"""create masks table

Revision ID: 4272dc77222e
Revises: 9be46877e434
Create Date: 2022-11-11 00:47:34.853055

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy_utils import TSVectorType

# revision identifiers, used by Alembic.
revision = '4272dc77222e'
down_revision = '9be46877e434'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'masks',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('pharmacy_id', sa.Integer, sa.ForeignKey('pharmacies.id')),
        sa.Column('name', sa.String, index=True),
        sa.Column('price', sa.Float, default=0),
        sa.Column('quantity', sa.Integer, default=0),
        sa.Column('color', sa.String),
        sa.Column('created_at', sa.DateTime, default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column('name_tsv', TSVectorType('name'), sa.Computed("to_tsvector('simple', \"name\")", persisted=True)),
    )


def downgrade() -> None:
    op.drop_constraint('masks_pharmacy_id_fkey', 'masks', type_='foreignkey')
    op.drop_table('masks')
