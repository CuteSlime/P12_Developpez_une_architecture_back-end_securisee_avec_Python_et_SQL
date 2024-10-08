from datetime import datetime
from typing import List, TYPE_CHECKING

from sqlalchemy import ForeignKey, func, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .model_base import Base
if TYPE_CHECKING:
    from Models import User, Contract, Event


class Customer(Base):
    """Customer of the company """

    __tablename__ = 'customers'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    information: Mapped[str] = mapped_column(String(1000), nullable=True)
    full_name: Mapped[str] = mapped_column(String(64), nullable=False)
    email: Mapped[str] = mapped_column(String(64), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(64), nullable=False)
    company_name: Mapped[str] = mapped_column(String(128), nullable=True)
    created_date: Mapped[datetime] = mapped_column(
        insert_default=func.now(), nullable=False)
    last_update: Mapped[datetime] = mapped_column(
        insert_default=func.now(), nullable=False)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False)

    sales_representative: Mapped["User"] = relationship(
        back_populates="customers")

    contracts: Mapped[List["Contract"]] = relationship(
        back_populates="customer_data")
    events: Mapped[List["Event"]] = relationship(
        back_populates="customer_data")
