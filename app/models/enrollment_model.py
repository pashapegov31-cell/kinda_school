from datetime import datetime

from pydantic import BaseModel, ConfigDict


class EnrollmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    course_id: int
    enrolled_at: datetime
    progress: float
    completed: bool
    completed_at: datetime
    updated_at: datetime
