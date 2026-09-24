from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.entities.course_entity import CourseStatus


class CourseCreate(BaseModel):
    title: str
    description: str
    price: Decimal


class CourseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    teacher_id: int
    title: str
    description: str
    price: Decimal
    status: CourseStatus
    created_at: datetime
