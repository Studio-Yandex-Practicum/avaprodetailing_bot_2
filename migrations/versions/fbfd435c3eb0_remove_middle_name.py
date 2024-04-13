"""remove middle name

Revision ID: fbfd435c3eb0
Revises: 4a50dd43ec91
Create Date: 2024-04-13 18:53:54.242505

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fbfd435c3eb0'
down_revision: Union[str, None] = '4a50dd43ec91'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'middle_name')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('middle_name', sa.VARCHAR(length=120), nullable=False))
    # ### end Alembic commands ###
