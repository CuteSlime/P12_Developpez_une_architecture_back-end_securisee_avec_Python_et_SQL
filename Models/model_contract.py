from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from Models import Customer


class Base(DeclarativeBase):
    pass


class Contract(Base):
    __tablename__ = 'contracts'

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    total_price: Mapped[float]
    remaining_to_pay: Mapped[float]
    contract_creation: Mapped[datetime] = mapped_column(
        insert_default=func.now()
    )
    statut: Mapped[bool]

    customer_data: Mapped["Customer"] = relationship(back_populates=)
