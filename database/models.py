from datetime import datetime

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class Lesson(Base):
    __tablename__ = 'lessons'
    id: Mapped[int] = mapped_column(primary_key=True)
    pupil_name: Mapped[str]
    date: Mapped[datetime] = mapped_column(default=datetime.date)
    time: Mapped[str] = mapped_column(default='09:00')
    comment: Mapped[str] = mapped_column(default='')
    is_audition: Mapped[bool] = mapped_column(default=False)
    __table_args__ = (UniqueConstraint('date', 'time', name='_date_time_unique'), )