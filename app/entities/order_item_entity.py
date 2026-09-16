from dataclasses import dataclass
from decimal import Decimal


@dataclass
class OrderItemEntity:
    id: int
    order_id: int
    product_id: int
    quantity: int
    price: Decimal
