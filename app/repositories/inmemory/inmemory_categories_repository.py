from app.entities.category_entity import CategoryEntity
from app.exceptions.exceptions import CantBeDeletedError


class InMemoryCategoryRepository:
    def __init__(self):
        self._categories: dict[int, CategoryEntity] = {}

    async def create(self, new_category: CategoryEntity) -> CategoryEntity:
        self._categories[new_category.id] = new_category
        return new_category

    async def get_by_name(self, name: str) -> CategoryEntity | None:
        for category in self._categories.values():
            if name == category.name:
                return category
        return None

    async def get_by_id(self, id: int) -> CategoryEntity | None:
        return self._categories.get(id)

    async def delete(self, data: CategoryEntity) -> CategoryEntity:
        category = self._categories[data.id]
        if not category:
            raise CantBeDeletedError("Такой позиции не существует")
        del self._categories[category.id]
        return category
