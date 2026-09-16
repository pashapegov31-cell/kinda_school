from dataclasses import dataclass


@dataclass
class CategoryEntity:
    id: int
    name: str
    parent_id: int | None
