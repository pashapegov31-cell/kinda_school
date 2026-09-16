from app.entities.product_entity import ProductEntity


class InMemoryProductsRepository:
    def __init__(self):
        self._products: dict[int, ProductEntity] = {}

    def create(self, new_product: ProductEntity) -> ProductEntity:
        self._products[new_product.id] = new_product
        return new_product

    def get_by_id(self, id: int) -> ProductEntity | None:
        return self._products[id] or None

    def get_by_name(self, name: str) -> ProductEntity | None:
        for product in self._products.values():
            if name == product.name:
                return product

        return None

    def delete(self, product: ProductEntity) -> ProductEntity:
        product = self._products[product.id]
        if not product:
            raise Exception("Такой позиции не существует")  #! create own exceptions
        del self._products[product.id]
        return product
