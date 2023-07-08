"""create initial tables

Revision ID: e8938d4a3580
Revises:
Create Date: 2023-07-08 18:35:52.235321

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "e8938d4a3580"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "command",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("data", sa.JSON(), nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
        sa.Column("target_name", sa.String(), sa.ForeignKey("target.name")),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "target",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("url", sa.String(255), nullable=False),
        sa.PrimaryKeyConstraint("name"),
    )


def downgrade():
    op.drop_table("command")
    op.drop_table("target")
