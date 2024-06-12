from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


if TYPE_CHECKING:
    from .person import Person
    from .product import Product


class Shop(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(20), unique=True)
    rating: Mapped[int] = mapped_column(nullable=True)

    products: Mapped[list["Product"]] = relationship(
        back_populates="shops", secondary="shop_assotiation_table"
    )
    workers: Mapped[list["Person"]] = relationship(back_populates="work_place")
