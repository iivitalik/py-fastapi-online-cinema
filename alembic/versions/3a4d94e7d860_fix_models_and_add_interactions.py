"""fix_models_and_add_interactions

Revision ID: 3a4d94e7d860
Revises: e93e3d6d3b3a
Create Date: 2025-12-29 22:26:09.816582

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3a4d94e7d860'
down_revision: Union[str, Sequence[str], None] = 'e93e3d6d3b3a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
