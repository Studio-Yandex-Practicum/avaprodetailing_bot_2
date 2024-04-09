"""empty message

Revision ID: 029f148c3832
Revises: 2e278124af37
Create Date: 2024-04-07 15:10:05.680588

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '029f148c3832'
down_revision: Union[str, None] = '2e278124af37'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
