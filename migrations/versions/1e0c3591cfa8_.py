"""empty message

Revision ID: 1e0c3591cfa8
Revises: 492c7569b4ab
Create Date: 2024-04-03 12:10:21.329968

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1e0c3591cfa8'
down_revision: Union[str, None] = '492c7569b4ab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
