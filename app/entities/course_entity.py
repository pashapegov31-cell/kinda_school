from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum


class CourseStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


@dataclass
class CourseEntity:
    id: int
    teacher_id: int
    title: str
    description: str
    price: Decimal
    status: CourseStatus
    created_at: datetime
    updated_at: datetime
