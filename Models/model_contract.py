from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .model_base import Base


class Contract(Base):
    __tablename__ = 'contracts'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    total_price: Mapped[float]
    remaining_to_pay: Mapped[float]
    contract_creation: Mapped[datetime] = mapped_column(
        insert_default=func.now()
    )
    statut: Mapped[bool]

    customer_data: Mapped["Customer"] = relationship(
        back_populates="contracts")

    events: Mapped[List["Event"]] = relationship(back_populates="contract")
