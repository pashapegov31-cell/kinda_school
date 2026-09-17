from app.entities.cart_item_entity import CartItemEntity
from app.exceptions.exceptions import CantBeDeletedError


class InMemoryCartItemsRepository:
    def __init__(self):
        self._cart_items: dict[int, CartItemEntity] = {}

    async def create(self, new_cart_item: CartItemEntity) -> CartItemEntity:
        self._cart_items[new_cart_item.id] = new_cart_item
        return new_cart_item

    async def get_by_id(self, id: int) -> CartItemEntity | None:
        return self._cart_items.get(id)

    async def delete(self, cart_item: CartItemEntity) -> CartItemEntity:
        cart_item = self._cart_items[cart_item.id]
        if not cart_item:
            raise CantBeDeletedError("Такой позиции не существует")
        del self._cart_items[cart_item.id]
        return cart_item

    # ? more methods to find a cart_item???
