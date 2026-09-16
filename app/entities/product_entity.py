from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class ProductEntity:
    id: int
    name: str
    description: str
    price: Decimal
    stock: int
    category_id: int
    created_at: datetime
