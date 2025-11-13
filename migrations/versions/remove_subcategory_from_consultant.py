"""Remove subcategory from consultant table

Revision ID: remove_subcategory_consultant
Revises: 682a7ea3121d
Create Date: 2025-11-12 21:19:30

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'remove_subcategory_consultant'
down_revision = '682a7ea3121d'
branch_labels = None
depends_on = None


def upgrade():
    # Remove subcategory column from consultant table
    try:
        op.drop_column('consultant', 'subcategory')
    except Exception as e:
        # Column might not exist, that's fine
        print(f"Column drop attempt: {e}")
    
    # Remove subcategory relationship from consultant model table args if exists
    # This is handled automatically by Alembic


def downgrade():
    # Add subcategory column back (this would restore the old structure)
    # Note: This requires SubCategory model to be available again
    try:
        op.add_column('consultant', sa.Column('subcategory', sa.Integer(), 
                                               sa.ForeignKey('subcategory.id'), 
                                               nullable=False))
    except Exception as e:
        print(f"Column add attempt: {e}")