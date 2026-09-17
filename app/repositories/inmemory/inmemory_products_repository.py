from app.entities.product_entity import ProductEntity
from app.exceptions.exceptions import CantBeDeletedError


class InMemoryProductsRepository:
    def __init__(self):
        self._products: dict[int, ProductEntity] = {}

    async def create(self, new_product: ProductEntity) -> ProductEntity:
        self._products[new_product.id] = new_product
        return new_product

    async def get_by_id(self, id: int) -> ProductEntity | None:
        return self._products.get(id)

    async def get_by_name(self, name: str) -> ProductEntity | None:
        for product in self._products.values():
            if name == product.name:
                return product

        return None

    async def delete(self, data: ProductEntity) -> ProductEntity:
        product = self._products[data.id]
        if not product:
            raise CantBeDeletedError("Такой позиции не существует")
        del self._products[product.id]
        return product
