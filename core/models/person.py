from .base import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class Person(Base):
    first_name: Mapped[str] = mapped_column(String(10))
    second_name: Mapped[str] = mapped_column(String(15))
    years: Mapped[int]
    username: Mapped[str] = mapped_column(String(10), unique=True)
    email: Mapped[str] = mapped_column(String(20))
