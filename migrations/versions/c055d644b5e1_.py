"""empty message

Revision ID: c055d644b5e1
Revises: b9b4bbb3aa2c
Create Date: 2024-04-10 00:22:54.138230

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c055d644b5e1'
down_revision: Union[str, None] = 'b9b4bbb3aa2c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
