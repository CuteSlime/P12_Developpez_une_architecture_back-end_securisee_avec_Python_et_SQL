from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Customer(Base):
    __tablename__ = 'customers'

    id: Mapped[int] = mapped_column(primary_key=True)
    information: Mapped[str]
    full_name: Mapped[str]
    email: Mapped[str]
    phone_number: Mapped[str]
    company_name: Mapped[str]
    created_date: Mapped[datetime] = mapped_column(insert_default=func.now())
    last_update: Mapped[datetime] = mapped_column(insert_default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    sales_representative: Mapped["User"] = relationship(
        back_populates="customers")

    contracts: Mapped[List["Contract"]] = relationship(
        back_populates="customers")
    events: Mapped[List["Event"]] = relationship(back_populates="customers")
