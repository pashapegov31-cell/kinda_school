from datetime import datetime

from pydantic import BaseModel


class EnrollmentResponse(BaseModel):
    id: int
    user_id: int
    course_id: int
    enrolled_at: datetime
    progress: float
    completed: bool
    completed_at: datetime
    updated_at: datetime
