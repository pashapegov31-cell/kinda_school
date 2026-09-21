from datetime import datetime

from pydantic import BaseModel


class LessonProgressCreate(BaseModel):
    enrollment_id: int
    lesson_id: int


class LessonProgressResponse(BaseModel):
    enrollment_id: int
    lesson_id: int
    completed: bool
    completed_at: datetime | None
