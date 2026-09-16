from typing import Protocol

from app.entities.order_item_entity import OrderItemEntity


class OrderItemsRepository(Protocol):
    async def create(self, new_order_item: OrderItemEntity) -> OrderItemEntity: ...
    async def get_by_id(self, id: int) -> OrderItemEntity | None: ...
