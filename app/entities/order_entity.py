from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from app.entities.order_item_entity import OrderItemEntity


@dataclass
class OrderEntity:
    id: int
    user_id: int
    items: list[OrderItemEntity]
    status: str
    total: Decimal
    created_at: datetime
