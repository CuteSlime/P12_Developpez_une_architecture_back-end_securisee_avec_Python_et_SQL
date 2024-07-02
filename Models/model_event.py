from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from Models import User, Contract, Customer


class Base(DeclarativeBase):
    pass


class Event(Base):
    __tablename__ = 'events'

    id: Mapped[int] = mapped_column(primary_key=True)
    contract_id: Mapped[int] = mapped_column(ForeignKey("contracts.id"))
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    event_start: Mapped[datetime]
    event_end: Mapped[datetime]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    location: Mapped[str]
    attendees: Mapped[int]
    notes: Mapped[str]

    contract: Mapped["Contract"] = relationship(back_populates=)
    customer_data: Mapped["Customer"] = relationship(back_populates=)
    support: Mapped["User"] = relationship(back_populates=)
