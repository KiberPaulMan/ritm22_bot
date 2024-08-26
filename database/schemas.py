from pydantic import BaseModel
from datetime import date


class LessonBase(BaseModel):
    pupil_name: str
    date: date
    time: str
    comment: str | None = None
    is_audition: bool = False


class LessonCreate(LessonBase):
    pass


class LessonEdit(LessonBase):
    pass


class Lesson(LessonBase):
    id: int

    class Config:
        from_attributes = True
