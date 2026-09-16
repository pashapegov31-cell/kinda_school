from decimal import Decimal

from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    description: str
    price: Decimal
    category: str


class ProductResponse(BaseModel):
    name: str
    description: str
    price: Decimal
    category: str
    stock: int
