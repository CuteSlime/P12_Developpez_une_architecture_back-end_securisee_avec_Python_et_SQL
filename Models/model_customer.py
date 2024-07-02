from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from Models import User


class Base(DeclarativeBase):
    pass


class Customer(Base):
    __tablename__ = 'Customers'

    id: Mapped[int] = mapped_column(primary_key=True)
    information: Mapped[str]
    full_name: Mapped[str]
    email: Mapped[str]
    phone_number: Mapped[str]
    company_name: Mapped[str]
    created_date: Mapped[datetime] = mapped_column(insert_default=func.now())
    last_update: Mapped[datetime] = mapped_column(insert_default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    sales_representative: Mapped["User"] = relationship(back_populates=)
