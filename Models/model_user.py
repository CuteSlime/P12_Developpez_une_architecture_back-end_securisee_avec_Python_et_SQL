from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str]
    email: Mapped[str]
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))

    role: Mapped["Group"] = relationship(back_populates="users")

    contracts: Mapped[List["Contract"]] = relationship(back_populates="users")
    customers: Mapped[List["Customer"]] = relationship(back_populates="users")
    events: Mapped[List["Event"]] = relationship(back_populates="users")