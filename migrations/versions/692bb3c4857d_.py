"""empty message

Revision ID: 692bb3c4857d
Revises: 1628c19f28b1
Create Date: 2024-04-16 21:27:14.967572

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '692bb3c4857d'
down_revision: Union[str, None] = '1628c19f28b1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
