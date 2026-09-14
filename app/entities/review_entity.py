from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class ReviewEntity:
    id: int
    user_id: int
    product_id: int
    rating: Decimal
    body: str
    created_at: datetime
