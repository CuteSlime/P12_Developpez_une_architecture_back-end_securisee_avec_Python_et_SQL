from datetime import datetime

from sqlalchemy import ForeignKey, String, SmallInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .model_base import Base


class Event(Base):
    """Event created by User for customer"""

    __tablename__ = 'events'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    contract_id: Mapped[int] = mapped_column(
        ForeignKey("contracts.id"), nullable=False)
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id"), nullable=False)
    event_start: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    event_end: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False)
    location: Mapped[str] = mapped_column(String(1000), nullable=False)
    attendees: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    notes: Mapped[str] = mapped_column(String(1000), nullable=True)

    contract: Mapped["Contract"] = relationship(back_populates="events")
    customer_data: Mapped["Customer"] = relationship(back_populates="events")
    support: Mapped["User"] = relationship(back_populates="events")
