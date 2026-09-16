from decimal import Decimal

from pydantic import BaseModel


class OrderItemCreate(BaseModel):
    order_id: int
    product_id: int
    quantity: int


class OrderItemResponse(BaseModel):
    order_id: int
    product_id: int
    quantity: int
    price: Decimal
