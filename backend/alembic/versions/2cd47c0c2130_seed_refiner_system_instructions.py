"""seed refiner system instructions

Revision ID: 2cd47c0c2130
Revises: c22e7fdc9ffb
Create Date: 2025-07-28 22:12:53.011988
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from app.core.instructions.refiner_instructions import REFINER_SYSTEM_INSTRUCTIONS

# revision identifiers, used by Alembic.
revision: str = '2cd47c0c2130'
down_revision: Union[str, Sequence[str], None] = 'c22e7fdc9ffb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Seed master refiner system instruction."""
    system_instructions_table = sa.table(
        'system_instructions',
        sa.column('role', sa.String),
        sa.column('type', sa.String),
        sa.column('instructions', sa.Text),
    )

    op.bulk_insert(system_instructions_table, [
        {
            'role': 'refiner',
            'type': 'master',
            'instructions': REFINER_SYSTEM_INSTRUCTIONS,
        },
    ])


def downgrade() -> None:
    """Remove refiner system instruction."""
    conn = op.get_bind()
    conn.execute(
        sa.text("""
            DELETE FROM system_instructions
            WHERE role = 'refiner' AND type = 'master'
        """)
    )
