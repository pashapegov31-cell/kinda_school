from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class CourseCreate(BaseModel):
    teacher_id: int
    title: str
    description: str
    price: Decimal


class CourseResponse(BaseModel):
    teacher_id: int
    title: str
    description: str
    price: Decimal
    created_at: datetime
