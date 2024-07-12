from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .model_base import Base


class Group(Base):
    __tablename__ = 'groups'

    id: Mapped[int] = mapped_column(primary_key=True)
    group_name: Mapped[str]

    users: Mapped[List["User"]] = relationship(back_populates="groups")
