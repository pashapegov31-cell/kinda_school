from datetime import datetime

from pydantic import BaseModel


class EnrollmentCreate(BaseModel):
    user_id: int
    course_id: int


class EnrollmentRepsonse(BaseModel):
    user_id: int
    course_id: int
    enrolled_at: datetime
    progress: float
    completed: bool
