from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database.models import Lesson
from database.database import get_engine
from database import crud


async def copy_lessons_to_day_via_week():
    current_date = datetime.now().date()
    next_date = current_date + timedelta(days=7)

    with Session(get_engine()) as session:
        lessons = session.query(Lesson).filter(Lesson.date == current_date)

        if lessons:
            for lesson in lessons:
                # Если занятие не является прослушиванием:
                if lesson.comment != '0':
                    lesson.date = next_date
                    crud.create_lesson(lesson)
    return None


# Create scheduler instance
scheduler = AsyncIOScheduler()

# Add task to scheduler
scheduler.add_job(
    copy_lessons_to_day_via_week,
    'cron',
    day_of_week='mon-sun',
    hour=7,
    minute=0,
    timezone='Asia/Barnaul',
    start_date=datetime.now(),
)
