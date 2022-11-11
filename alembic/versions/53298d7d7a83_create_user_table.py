"""create user table

Revision ID: 53298d7d7a83
Revises: 
Create Date: 2022-11-10 15:42:40.655019

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '53298d7d7a83'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('email', sa.String, unique=True, index=True),
        sa.Column('name', sa.String),
        sa.Column('hashed_password', sa.String),
        sa.Column('cash_balance', sa.Float, default=0),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('created_at', sa.DateTime, default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, default=sa.func.now(), onupdate=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('users')
