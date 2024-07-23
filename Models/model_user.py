from typing import List

from argon2 import PasswordHasher
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .model_base import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(64), nullable=False)
    email: Mapped[str] = mapped_column(String(64), nullable=False)
    password: Mapped[str] = mapped_column(String(256), nullable=False)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))

    role: Mapped["Group"] = relationship(back_populates="users")

    customers: Mapped[List["Customer"]] = relationship(
        back_populates="sales_representative")
    events: Mapped[List["Event"]] = relationship(back_populates="support")

    def set_password(self, password):
        ph = PasswordHasher()
        self.password = ph.hash(password)

    def check_password(self, password):
        ph = PasswordHasher()
        return ph.verify(self.password, password)
