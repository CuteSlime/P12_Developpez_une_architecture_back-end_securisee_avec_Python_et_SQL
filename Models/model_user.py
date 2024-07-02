from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from Models import Group


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str]
    email: Mapped[str]
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))

    role: Mapped["Group"] = relationship(back_populates=)
