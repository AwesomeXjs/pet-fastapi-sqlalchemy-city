from typing import TYPE_CHECKING

from .base import Base
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .shop import Shop


class Person(Base):
    first_name: Mapped[str] = mapped_column(String(10))
    second_name: Mapped[str] = mapped_column(String(15))
    years: Mapped[int]
    username: Mapped[str] = mapped_column(String(10), unique=True)
    email: Mapped[str] = mapped_column(String(20))

    work_place_id: Mapped[int] = mapped_column(ForeignKey("shops.id"))
    work_place: Mapped["Shop"] = relationship(back_populates="workers")
