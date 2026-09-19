from dataclasses import dataclass
from datetime import datetime


@dataclass
class LessonProgressEntity:
    id: int
    enrollment_id: int
    lesson_id: int
    completed: bool
    completed_at: datetime | None
