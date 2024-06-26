"""create tables

Revision ID: cb5f009ca544
Revises: 
Create Date: 2024-06-12 18:08:28.614548

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "cb5f009ca544"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=50), nullable=False),
        sa.Column("type", sa.String(), nullable=False),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("title"),
    )
    op.create_table(
        "shops",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=20), nullable=False),
        sa.Column("rating", sa.Integer(), nullable=True),
        sa.Column("compensation", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("title"),
    )
    op.create_table(
        "persons",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("first_name", sa.String(length=10), nullable=False),
        sa.Column("second_name", sa.String(length=15), nullable=False),
        sa.Column("years", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=10), nullable=False),
        sa.Column("email", sa.String(length=50), nullable=False),
        sa.Column("work_place_name", sa.String(length=20), nullable=True),
        sa.ForeignKeyConstraint(
            ["work_place_name"],
            ["shops.title"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("username"),
    )
    op.create_table(
        "shop_assotiation_table",
        sa.Column("product_title", sa.String(length=50), nullable=False),
        sa.Column("shop_title", sa.String(length=20), nullable=False),
        sa.ForeignKeyConstraint(
            ["product_title"], ["products.title"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["shop_title"], ["shops.title"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("product_title", "shop_title"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("shop_assotiation_table")
    op.drop_table("persons")
    op.drop_table("shops")
    op.drop_table("products")
    # ### end Alembic commands ###
