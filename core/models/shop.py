from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


if TYPE_CHECKING:
    from .person import Person


class Shop(Base):
    title: Mapped[str] = mapped_column(String(20), unique=True)
    products: Mapped[str]
    rating: Mapped[int] = mapped_column(nullable=True)

    workers: Mapped[list["Person"]] = relationship(back_populates="work_place")
