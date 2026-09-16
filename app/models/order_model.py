from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class OrderCreate(BaseModel):
    user_id: int
    total: Decimal


class OrderResponse(BaseModel):
    user_id: int
    total: Decimal
    created_at: datetime
