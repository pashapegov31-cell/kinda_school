from dataclasses import dataclass


@dataclass
class CartItemEntity:
    id: int
    user_id: int
    product_id: int
    quantity: int
