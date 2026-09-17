from app.entities.order_item_entity import OrderItemEntity


class InMemoryOrderItemsRepository:
    def __init__(self):
        self._order_items: dict[int, OrderItemEntity] = {}

    async def create(self, new_order_item: OrderItemEntity) -> OrderItemEntity:
        self._order_items[new_order_item.id] = new_order_item
        return new_order_item

    async def get_by_id(self, id: int) -> OrderItemEntity | None:
        return self._order_items.get(id)

    # ? more methods???
