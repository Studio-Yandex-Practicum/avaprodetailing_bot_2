"""empty message

Revision ID: 91516996aff4
Revises: b534e48937b3
Create Date: 2024-04-21 13:48:24.931084

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '91516996aff4'
down_revision: Union[str, None] = 'b534e48937b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
