from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class PaymentEntity:
    id: int
    order_id: int
    amount: Decimal
    method: str
    status: str
    paid_at: datetime
