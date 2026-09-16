from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserEntity:
    id: int
    email: str
    name: str
    hashed_password: str
    created_at: datetime
