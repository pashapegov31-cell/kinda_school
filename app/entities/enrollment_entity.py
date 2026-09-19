from dataclasses import dataclass
from datetime import datetime


@dataclass
class EnrollmentEntity:
    id: int
    user_id: int
    course_id: int
    enrolled_at: datetime
    progress: float
    completed: bool
    completed_at: datetime | None
