from pydantic import BaseModel, ConfigDict, EmailStr

from app.entities.user_entity import UserRole


class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str


class ChangeUserRole(BaseModel):
    user_id: int
    new_role: UserRole


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    name: str
    role: UserRole


class UserUpdate(BaseModel):
    email: EmailStr
    name: str
    password: str
