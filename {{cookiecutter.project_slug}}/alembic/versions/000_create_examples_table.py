{% if cookiecutter.use_postgresql == "yes" -%}
"""Create examples table

Revision ID: 000_create_examples
Revises: 
Create Date: 2025-11-25

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '000_create_examples'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create examples table."""
    op.create_table(
        'examples',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_examples_id'), 'examples', ['id'], unique=False)
    op.create_index(op.f('ix_examples_name'), 'examples', ['name'], unique=False)


def downgrade() -> None:
    """Drop examples table."""
    op.drop_index(op.f('ix_examples_name'), table_name='examples')
    op.drop_index(op.f('ix_examples_id'), table_name='examples')
    op.drop_table('examples')
{% else -%}
"""Migration placeholder - PostgreSQL not enabled."""

# Migration disabled in this configuration
# To enable, regenerate with use_postgresql=yes
{% endif -%}
