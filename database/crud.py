from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.orm.query import Query
from database.models import Lesson
from database.schemas import LessonCreate, LessonEdit
from database.database import get_engine


def create_lesson(lesson: LessonCreate):
    with Session(get_engine()) as session:
        db_lesson = Lesson(
            pupil_name=lesson.pupil_name,
            date=lesson.date,
            time=lesson.time,
            comment=lesson.comment,
            is_audition=lesson.is_audition
        )
        try:
            session.add(db_lesson)
            session.commit()
            session.refresh(db_lesson)
            return db_lesson
        except:
            return None


def edit_lesson(my_date: str, my_time: str, lesson: LessonEdit):
    with Session(get_engine()) as session:
        current_lesson = session.query(Lesson).filter(Lesson.date == my_date, Lesson.time == my_time).first()
        try:
            current_lesson.pupil_name = lesson.pupil_name
            current_lesson.date = lesson.date
            current_lesson.time = lesson.time
            current_lesson.is_audition = False
            current_lesson.comment = lesson.comment
            session.commit()
            session.refresh(current_lesson)
            return current_lesson
        except:
            return None


def delete_lesson(my_date: datetime.date, my_time: str):
    with Session(get_engine()) as session:
        lesson = session.query(Lesson).filter(Lesson.date == my_date, Lesson.time == my_time).first()
        try:
            session.delete(lesson)
            session.commit()
            return 'Урок был удален!'
        except:
            return None


def get_week_timetable(date_start: datetime.date, date_end: datetime.date) -> Query:
    with Session(get_engine()) as session:
        return session \
            .query(Lesson) \
            .filter(Lesson.date >= date_start, Lesson.date <= date_end) \
            .order_by(Lesson.date, Lesson.time)


def get_list_times_by_date(my_date: str) -> list:
    with Session(get_engine()) as session:
        query = session.query(Lesson).filter(Lesson.date == my_date).order_by(Lesson.time)
        return query.with_entities(Lesson.time)


def get_lesson_by_date_and_time(my_date: datetime.date, my_time: str) -> Query:
    with Session(get_engine()) as session:
        return session.query(Lesson).filter(Lesson.date == my_date, Lesson.time == my_time).first()
