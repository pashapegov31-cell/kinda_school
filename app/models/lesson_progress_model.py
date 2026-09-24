from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LessonProgressCreate(BaseModel):
    enrollment_id: int
    lesson_id: int


class LessonProgressResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    enrollment_id: int
    lesson_id: int
    completed: bool
    completed_at: datetime | None
