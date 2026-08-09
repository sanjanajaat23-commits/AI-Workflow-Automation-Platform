"""add workflow schedules

Revision ID: d33d1e38cf8f
Revises: 077bfe240f7e
Create Date: 2026-07-31 18:33:41.644764
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "d33d1e38cf8f"
down_revision: Union[str, Sequence[str], None] = "077bfe240f7e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
        "workflow_schedules",

        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
        ),

        sa.Column(
            "workflow_id",
            sa.Integer(),
            sa.ForeignKey(
                "workflows.id",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),

        sa.Column(
            "cron",
            sa.String(length=100),
            nullable=False,
        ),

        sa.Column(
            "enabled",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
    )


def downgrade() -> None:

    op.drop_table("workflow_schedules")