from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from core.models.base import Base


class Message(Base):
    # id: Mapped[int] = mapped_column(primary_key=True)
    # message: Mapped[str]
    id = Column(Integer, primary_key=True)
    message = Column(String)

    # sqlalchemy to json
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
