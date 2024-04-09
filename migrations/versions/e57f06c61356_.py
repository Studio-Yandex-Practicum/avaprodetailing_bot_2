"""empty message

Revision ID: e57f06c61356
Revises: 85bb5811354d
Create Date: 2024-04-10 00:09:53.107379

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e57f06c61356'
down_revision: Union[str, None] = '85bb5811354d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
