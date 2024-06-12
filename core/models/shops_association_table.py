from .base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class ShopsAssotiationTable(Base):
    __tablename__ = "shop_assotiation_table"

    product_title: Mapped[int] = mapped_column(
        ForeignKey("products.title", ondelete="CASCADE"), primary_key=True
    )
    shop_title: Mapped[int] = mapped_column(
        ForeignKey("shops.title", ondelete="CASCADE"), primary_key=True
    )
