from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    name: str
    password: str


class UserResponse(BaseModel):
    email: str
    name: str


class UserUpdate(BaseModel):
    email: str
    name: str
    password: str
