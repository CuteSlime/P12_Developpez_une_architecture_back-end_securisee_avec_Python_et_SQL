from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey, func, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .model_base import Base


class Contract(Base):
    __tablename__ = 'contracts'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id"), nullable=False)
    total_price: Mapped[float] = mapped_column(Float, nullable=False)
    remaining_to_pay: Mapped[float] = mapped_column(Float, nullable=False)
    contract_creation: Mapped[datetime] = mapped_column(
        insert_default=func.now(), nullable=False
    )
    statut: Mapped[bool] = mapped_column(
        Boolean, insert_default=False, nullable=False)

    customer_data: Mapped["Customer"] = relationship(
        back_populates="contracts")

    events: Mapped[List["Event"]] = relationship(back_populates="contract")
