"""empty message

Revision ID: e6c7f1f76e2c
Revises: c055d644b5e1
Create Date: 2024-04-10 00:24:41.219312

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e6c7f1f76e2c'
down_revision: Union[str, None] = 'c055d644b5e1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
