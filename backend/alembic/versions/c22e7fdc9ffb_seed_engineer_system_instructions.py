"""seed engineer system instructions

Revision ID: c22e7fdc9ffb
Revises: 081188d015ba
Create Date: 2025-07-28 22:08:28.028070
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from app.core.instructions.engineer_instructions import ENGINEER_SYSTEM_INSTRUCTIONS

# revision identifiers, used by Alembic.
revision: str = 'c22e7fdc9ffb'
down_revision: Union[str, Sequence[str], None] = '081188d015ba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Seed master engineer system instruction."""
    system_instructions_table = sa.table(
        'system_instructions',
        sa.column('role', sa.String),
        sa.column('type', sa.String),
        sa.column('instructions', sa.Text),
    )

    op.bulk_insert(system_instructions_table, [
        {
            'role': 'engineer',
            'type': 'master',
            'instructions': ENGINEER_SYSTEM_INSTRUCTIONS,
        },
    ])


def downgrade() -> None:
    """Remove engineer system instruction."""
    conn = op.get_bind()
    conn.execute(
        sa.text("""
            DELETE FROM system_instructions
            WHERE role = 'engineer' AND type = 'master'
        """)
    )
