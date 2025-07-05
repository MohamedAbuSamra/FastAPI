"""Add foreign key from products.location to countries.iso

Revision ID: c5e8cc359327
Revises: a14c9b66e4d1
Create Date: 2025-07-05 09:04:29.763266

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c5e8cc359327'
down_revision = 'a14c9b66e4d1'
branch_labels = None
depends_on = None


def upgrade():
    op.create_foreign_key(
        'products_location_fkey',
        'products', 'countries',
        ['location'], ['iso']
    )


def downgrade():
    op.drop_constraint('products_location_fkey', 'products', type_='foreignkey')