from app.entities.order_entity import OrderEntity


class InMemoryOrdersRepository:
    def __init__(self):
        self._orders: dict[int, OrderEntity] = {}

    def create(self, new_order: OrderEntity) -> OrderEntity:
        self._orders[new_order.id] = new_order
        return new_order

    def get_by_id(self, id: int) -> OrderEntity | None:
        return self._orders[id] or None

    # ? more methods???
