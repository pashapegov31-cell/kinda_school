from typing import Protocol

from app.entities.order_entity import OrderEntity


class OrdersRepository(Protocol):
    async def create(self, new_order: OrderEntity) -> OrderEntity: ...
    async def get_by_id(self, id: int) -> OrderEntity: ...
