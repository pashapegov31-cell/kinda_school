from dataclasses import dataclass


@dataclass
class CartItemEntity:
    id: int
    cart_id: int
    product_id: int
    quantity: int
