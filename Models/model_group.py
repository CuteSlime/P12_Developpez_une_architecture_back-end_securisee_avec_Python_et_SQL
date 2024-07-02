from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Group(Base):
    __tablename__ = 'groups'

    id: Mapped[int] = mapped_column(primary_key=True)
    group_name: Mapped[str]
