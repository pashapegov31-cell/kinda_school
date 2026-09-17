from dataclasses import dataclass

from app.entities.cart_item_entity import CartItemEntity


@dataclass
class CartEntity:
    id: int
    user_id: int
    items: list[CartItemEntity]
