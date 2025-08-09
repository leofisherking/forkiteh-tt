"""requests

Revision ID: 15762ec418e7
Revises:
Create Date: 2025-08-07 20:20:34.572200

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from forkiteh.core.settings import settings

# revision identifiers, used by Alembic.
revision: str = "15762ec418e7"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "requests",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("wallet_address", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("timezone('UTC', now())"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        schema=settings.POSTGRES_SCHEMA,
    )
    op.create_index(
        op.f(f"ix_{settings.POSTGRES_SCHEMA}_requests_wallet_address"),
        "requests",
        ["wallet_address"],
        unique=False,
        schema=settings.POSTGRES_SCHEMA,
    )


def downgrade() -> None:
    op.drop_index(
        op.f(f"ix_{settings.POSTGRES_SCHEMA}_requests_wallet_address"),
        table_name="requests",
        schema=settings.POSTGRES_SCHEMA,
    )
    op.drop_table("requests", schema=settings.POSTGRES_SCHEMA)
