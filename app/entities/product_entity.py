from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from app.entities.category_entity import CategoryEntity


@dataclass
class ProductEntity:
    id: int
    name: str
    description: str
    price: Decimal
    stock: int
    category: CategoryEntity
    created_at: datetime
