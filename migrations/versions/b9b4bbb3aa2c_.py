"""empty message

Revision ID: b9b4bbb3aa2c
Revises: d486f9f2f62a
Create Date: 2024-04-10 00:21:47.410520

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b9b4bbb3aa2c'
down_revision: Union[str, None] = 'd486f9f2f62a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
