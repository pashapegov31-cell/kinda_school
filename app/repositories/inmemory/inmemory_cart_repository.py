from app.entities.cart_entity import CartEntity


class InMemoryCartRepository:
    def __init__(self):
        self._carts: dict[int, CartEntity] = {}

    async def create(self, new_cart: CartEntity) -> CartEntity:
        self._carts[new_cart.id] = new_cart
        return new_cart

    async def get_by_user_id(self, user_id: int) -> CartEntity | None:
        for cart in self._carts.values():
            if cart.user_id == user_id:
                return cart
        return None

    async def get_by_id(self, id: int) -> CartEntity | None:
        return self._carts.get(id)
