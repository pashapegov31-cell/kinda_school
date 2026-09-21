from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from app.entities.course_entity import CourseStatus


class CourseCreate(BaseModel):
    title: str
    description: str
    price: Decimal


class CourseResponse(BaseModel):
    id: int
    teacher_id: int
    title: str
    description: str
    price: Decimal
    status: CourseStatus
    created_at: datetime
