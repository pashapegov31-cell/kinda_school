from pydantic import BaseModel, EmailStr

from app.entities.user_entity import UserRole


class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    email: EmailStr
    name: str
    role: UserRole


class UserUpdate(BaseModel):
    email: EmailStr
    name: str
    password: str
