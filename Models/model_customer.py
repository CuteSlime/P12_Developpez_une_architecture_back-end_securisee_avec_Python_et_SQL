from datetime import datetime
from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from .model_base import Base


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
