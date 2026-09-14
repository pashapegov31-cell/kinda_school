from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class OrderEntity:
    id: int
    user_id: int
    status: str
    total: Decimal
    created_at: datetime
