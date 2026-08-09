"""create workflow system tables

Revision ID: 077bfe240f7e
Revises:
Create Date: 2026-07-24 02:13:16.567833
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# Revision identifiers used by Alembic.
revision: str = "077bfe240f7e"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "workflows",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_workflows_id"),
        "workflows",
        ["id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_workflows_user_id"),
        "workflows",
        ["user_id"],
        unique=False,
    )

    op.create_table(
        "executions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("workflow_id", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("input_data", sa.JSON(), nullable=True),
        sa.Column("output_data", sa.JSON(), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["workflow_id"],
            ["workflows.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_executions_id"),
        "executions",
        ["id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_executions_workflow_id"),
        "executions",
        ["workflow_id"],
        unique=False,
    )

    op.create_table(
        "workflow_connections",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("workflow_id", sa.Integer(), nullable=False),
        sa.Column("source_node_key", sa.String(length=255), nullable=False),
        sa.Column("target_node_key", sa.String(length=255), nullable=False),
        sa.Column("source_handle", sa.String(length=255), nullable=True),
        sa.Column("target_handle", sa.String(length=255), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["workflow_id"],
            ["workflows.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_workflow_connections_id"),
        "workflow_connections",
        ["id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_workflow_connections_workflow_id"),
        "workflow_connections",
        ["workflow_id"],
        unique=False,
    )

    op.create_table(
        "workflow_nodes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("workflow_id", sa.Integer(), nullable=False),
        sa.Column("node_key", sa.String(length=255), nullable=False),
        sa.Column("node_type", sa.String(length=100), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("config", sa.JSON(), nullable=False),
        sa.Column("position_x", sa.Integer(), nullable=True),
        sa.Column("position_y", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["workflow_id"],
            ["workflows.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_workflow_nodes_id"),
        "workflow_nodes",
        ["id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_workflow_nodes_workflow_id"),
        "workflow_nodes",
        ["workflow_id"],
        unique=False,
    )

    op.create_table(
        "execution_logs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("execution_id", sa.Integer(), nullable=False),
        sa.Column("node_key", sa.String(length=255), nullable=True),
        sa.Column("level", sa.String(length=50), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("data", sa.JSON(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["execution_id"],
            ["executions.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_execution_logs_execution_id"),
        "execution_logs",
        ["execution_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_execution_logs_id"),
        "execution_logs",
        ["id"],
        unique=False,
    )

    # Fill existing NULL values before applying NOT NULL constraints.
    op.execute(
        sa.text(
            "UPDATE users "
            "SET is_active = 1 "
            "WHERE is_active IS NULL"
        )
    )

    op.execute(
        sa.text(
            "UPDATE users "
            "SET created_at = CURRENT_TIMESTAMP "
            "WHERE created_at IS NULL"
        )
    )

    op.execute(
        sa.text(
            "UPDATE users "
            "SET updated_at = CURRENT_TIMESTAMP "
            "WHERE updated_at IS NULL"
        )
    )

    # SQLite requires batch mode to alter existing columns.
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.alter_column(
            "is_active",
            existing_type=sa.Boolean(),
            nullable=False,
        )

        batch_op.alter_column(
            "created_at",
            existing_type=sa.DateTime(),
            nullable=False,
        )

        batch_op.alter_column(
            "updated_at",
            existing_type=sa.DateTime(),
            nullable=False,
        )

    op.create_index(
        op.f("ix_users_email"),
        "users",
        ["email"],
        unique=True,
    )

    op.create_index(
        op.f("ix_users_username"),
        "users",
        ["username"],
        unique=True,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(
        op.f("ix_users_username"),
        table_name="users",
    )

    op.drop_index(
        op.f("ix_users_email"),
        table_name="users",
    )

    # SQLite requires batch mode to alter existing columns.
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.alter_column(
            "updated_at",
            existing_type=sa.DateTime(),
            nullable=True,
        )

        batch_op.alter_column(
            "created_at",
            existing_type=sa.DateTime(),
            nullable=True,
        )

        batch_op.alter_column(
            "is_active",
            existing_type=sa.Boolean(),
            nullable=True,
        )

    op.drop_index(
        op.f("ix_execution_logs_id"),
        table_name="execution_logs",
    )

    op.drop_index(
        op.f("ix_execution_logs_execution_id"),
        table_name="execution_logs",
    )

    op.drop_table("execution_logs")

    op.drop_index(
        op.f("ix_workflow_nodes_workflow_id"),
        table_name="workflow_nodes",
    )

    op.drop_index(
        op.f("ix_workflow_nodes_id"),
        table_name="workflow_nodes",
    )

    op.drop_table("workflow_nodes")

    op.drop_index(
        op.f("ix_workflow_connections_workflow_id"),
        table_name="workflow_connections",
    )

    op.drop_index(
        op.f("ix_workflow_connections_id"),
        table_name="workflow_connections",
    )

    op.drop_table("workflow_connections")

    op.drop_index(
        op.f("ix_executions_workflow_id"),
        table_name="executions",
    )

    op.drop_index(
        op.f("ix_executions_id"),
        table_name="executions",
    )

    op.drop_table("executions")

    op.drop_index(
        op.f("ix_workflows_user_id"),
        table_name="workflows",
    )

    op.drop_index(
        op.f("ix_workflows_id"),
        table_name="workflows",
    )

    op.drop_table("workflows")