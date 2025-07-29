"""seed grader system instructions

Revision ID: 62fdd473cd06
Revises: 4ed950d61fa3
Create Date: 2025-07-28 19:43:09.306243

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app.core.instructions.grader_instructions import (
    CLARITY_GRADER_SYSTEM_INSTRUCTIONS,
    SPECIFICITY_GRADER_SYSTEM_INSTRUCTIONS,
    COMPLEXITY_GRADER_SYSTEM_INSTRUCTIONS,
    COMPLETENESS_GRADER_SYSTEM_INSTRUCTIONS,
    CONSISTENCY_GRADER_SYSTEM_INSTRUCTIONS,
    MASTER_GRADER_SYSTEM_INSTRUCTIONS,
)



# revision identifiers, used by Alembic.
revision: str = '62fdd473cd06'
down_revision: Union[str, Sequence[str], None] = '4ed950d61fa3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    system_instructions_table = sa.table(
        'system_instructions',
        sa.column('role', sa.String),
        sa.column('type', sa.String),
        sa.column('instructions', sa.Text),
    )
    op.bulk_insert(system_instructions_table, [
        {
            'role': 'grader',
            'type': 'clarity',
            'instructions': CLARITY_GRADER_SYSTEM_INSTRUCTIONS,
        },
        {
            'role': 'grader',
            'type': 'specificity',
            'instructions': SPECIFICITY_GRADER_SYSTEM_INSTRUCTIONS,
        },
        {
            'role': 'grader',
            'type': 'complexity',
            'instructions': COMPLEXITY_GRADER_SYSTEM_INSTRUCTIONS,
        },
        {
            'role': 'grader',
            'type': 'completeness',
            'instructions': COMPLETENESS_GRADER_SYSTEM_INSTRUCTIONS,
        },
        {
            'role': 'grader',
            'type': 'consistency',
            'instructions': CONSISTENCY_GRADER_SYSTEM_INSTRUCTIONS,
        },
        {
            'role': 'grader',
            'type': 'master',
            'instructions': MASTER_GRADER_SYSTEM_INSTRUCTIONS,
        },
    ])



def downgrade() -> None:
    """Downgrade schema by removing seeded system instructions."""
    conn = op.get_bind()
    conn.execute(
        sa.text("""
            DELETE FROM system_instructions
            WHERE role = 'grader' AND type IN (
                'clarity',
                'specificity',
                'complexity',
                'completeness',
                'consistency',
                'master'
            )
        """)
    )
