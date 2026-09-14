from dataclasses import dataclass
from datetime import datetime

from pydantic import EmailStr


@dataclass
class UserEntity:
    id: int
    email: EmailStr
    firstname: str
    secondname: str
    hashed_password: str
    created_at: datetime
