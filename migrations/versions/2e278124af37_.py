"""empty message

Revision ID: 2e278124af37
Revises: 1c96d75af556
Create Date: 2024-04-07 15:08:55.662989

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2e278124af37'
down_revision: Union[str, None] = '1c96d75af556'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
