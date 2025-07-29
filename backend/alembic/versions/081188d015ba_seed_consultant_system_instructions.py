"""seed consultant system instructions

Revision ID: 081188d015ba
Revises: 62fdd473cd06
Create Date: 2025-07-28 21:00:25.558281

"""
from typing import Sequence, Union
from app.core.instructions.consultant_instructions import (
    CLARITY_CONSULTANT_SYSTEM_INSTRUCTIONS,
    SPECIFICITY_CONSULTANT_SYSTEM_INSTRUCTIONS,
    COMPLEXITY_CONSULTANT_SYSTEM_INSTRUCTIONS,
    COMPLETENESS_CONSULTANT_SYSTEM_INSTRUCTIONS,
    CONSISTENCY_CONSULTANT_SYSTEM_INSTRUCTIONS,
    MASTER_CONSULTANT_SYSTEM_INSTRUCTIONS,
)
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '081188d015ba'
down_revision: Union[str, Sequence[str], None] = '62fdd473cd06'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Seed consultant system instructions."""
    system_instructions_table = sa.table(
        'system_instructions',
        sa.column('role', sa.String),
        sa.column('type', sa.String),
        sa.column('instructions', sa.Text),
    )
    op.bulk_insert(system_instructions_table, [
        {
            'role': 'consultant',
            'type': 'clarity',
            'instructions': CLARITY_CONSULTANT_SYSTEM_INSTRUCTIONS,
        },
        {
            'role': 'consultant',
            'type': 'specificity',
            'instructions': SPECIFICITY_CONSULTANT_SYSTEM_INSTRUCTIONS,
        },
        {
            'role': 'consultant',
            'type': 'complexity',
            'instructions': COMPLEXITY_CONSULTANT_SYSTEM_INSTRUCTIONS,
        },
        {
            'role': 'consultant',
            'type': 'completeness',
            'instructions': COMPLETENESS_CONSULTANT_SYSTEM_INSTRUCTIONS,
        },
        {
            'role': 'consultant',
            'type': 'consistency',
            'instructions': CONSISTENCY_CONSULTANT_SYSTEM_INSTRUCTIONS,
        },
        {
            'role': 'consultant',
            'type': 'master',
            'instructions': MASTER_CONSULTANT_SYSTEM_INSTRUCTIONS,
        },
    ])

def downgrade() -> None:
    """Remove consultant system instructions."""
    conn = op.get_bind()
    conn.execute(
        sa.text("""
            DELETE FROM system_instructions
            WHERE role = 'consultant' AND type IN (
                'clarity',
                'specificity',
                'complexity',
                'completeness',
                'consistency',
                'master'
            )
        """)
    )
