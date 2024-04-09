"""empty message

Revision ID: 590899e4789d
Revises: 48204c0ebc39
Create Date: 2024-04-10 01:33:04.796629

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '590899e4789d'
down_revision: Union[str, None] = '48204c0ebc39'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
