from pydantic import BaseModel


class CategoryCreate(BaseModel):
    name: str
    parent_category_id: int


class CategoryResponse(BaseModel):
    name: str
