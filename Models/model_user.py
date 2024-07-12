from typing import List

from argon2 import PasswordHasher
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .model_base import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))

    role: Mapped["Group"] = relationship(back_populates="users")

    contracts: Mapped[List["Contract"]] = relationship(back_populates="users")
    customers: Mapped[List["Customer"]] = relationship(back_populates="users")
    events: Mapped[List["Event"]] = relationship(back_populates="users")

    def set_password(self, password):
        ph = PasswordHasher()
        self.password = ph.hash(password)

    def check_password(self, password):
        ph = PasswordHasher()
        return ph.verify(self.password, password)
