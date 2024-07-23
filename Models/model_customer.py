from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey, func, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .model_base import Base


class Customer(Base):
    __tablename__ = 'customers'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    information: Mapped[str] = mapped_column(String(1000), nullable=True)
    full_name: Mapped[str] = mapped_column(String(64), nullable=False)
    email: Mapped[str] = mapped_column(String(64), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(64), nullable=False)
    company_name: Mapped[str] = mapped_column(String(128), nullable=True)
    created_date: Mapped[datetime] = mapped_column(insert_default=func.now())
    last_update: Mapped[datetime] = mapped_column(insert_default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    sales_representative: Mapped["User"] = relationship(
        back_populates="customers")

    contracts: Mapped[List["Contract"]] = relationship(
        back_populates="customer_data")
    events: Mapped[List["Event"]] = relationship(
        back_populates="customer_data")
