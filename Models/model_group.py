from typing import List, TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .model_base import Base
if TYPE_CHECKING:
    from Models import User


class Group(Base):
    """Group used to manage permission """

    __tablename__ = 'groups'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    group_name: Mapped[str] = mapped_column(String(64), nullable=False)

    users: Mapped[List["User"]] = relationship(back_populates="role")
