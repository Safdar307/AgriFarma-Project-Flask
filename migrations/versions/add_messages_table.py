"""add messages table

Revision ID: add_messages_table
Revises: add_likes_tags_001
Create Date: 2025-11-10 21:59:59.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'add_messages_table'
down_revision = 'add_likes_tags_001'
branch_labels = None
depends_on = None


def upgrade():
    # Create messages table
    op.create_table('messages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=120), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create index for created_at for better query performance
    op.create_index('ix_messages_created_at', 'messages', ['created_at'], unique=False)
    
    # Create index for status for filtering
    op.create_index('ix_messages_status', 'messages', ['status'], unique=False)


def downgrade():
    # Drop indexes
    op.drop_index('ix_messages_status', table_name='messages')
    op.drop_index('ix_messages_created_at', table_name='messages')
    
    # Drop table
    op.drop_table('messages')