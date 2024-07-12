from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from .model_base import Base


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

    contract: Mapped["Contract"] = relationship(back_populates="events")
    customer_data: Mapped["Customer"] = relationship(back_populates="events")
    support: Mapped["User"] = relationship(back_populates="events")
