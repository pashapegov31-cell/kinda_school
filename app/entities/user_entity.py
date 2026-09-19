from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    TEACHER = "teacher"
    STUDENT = "student"
    ADMIN = "admin"


@dataclass
class UserEntity:
    id: int
    email: str
    name: str
    role: UserRole
    hashed_password: str
    created_at: datetime
