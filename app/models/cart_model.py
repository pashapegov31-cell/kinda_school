from pydantic import BaseModel


class CartCreate(BaseModel):
    user_id: int


class CartResponse(BaseModel):
    user_id: int
