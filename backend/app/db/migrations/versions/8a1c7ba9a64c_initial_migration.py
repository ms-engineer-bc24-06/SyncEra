"""Initial migration

Revision ID: 8a1c7ba9a64c
Revises: 5781c8d8dfc5
Create Date: 2024-08-14 07:48:37.499629

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8a1c7ba9a64c'
down_revision: Union[str, None] = '5781c8d8dfc5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
