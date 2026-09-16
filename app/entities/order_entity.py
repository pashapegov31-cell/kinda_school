from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum, auto

from app.entities.order_item_entity import OrderItemEntity


class OrderStatus(Enum):
    PENDING = auto()
    PAID = auto()
    SHIPPED = auto()
    CANCELLED = auto()


@dataclass
class OrderEntity:
    id: int
    user_id: int
    items: list[OrderItemEntity]
    status: OrderStatus
    total: Decimal
    created_at: datetime
    updated_at: datetime | None
