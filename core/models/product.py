from typing import TYPE_CHECKING

from enum import Enum
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


from .base import Base

if TYPE_CHECKING:
    from .shop import Shop


class Product(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50), unique=True)
    type: Mapped[str]
    price: Mapped[int]

    shops: Mapped[list["Shop"]] = relationship(
        back_populates="products",
        secondary="shop_assotiation_table",
    )
