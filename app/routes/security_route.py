from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_current_user_id, get_inmemory_users_repo
from app.models.user_model import UserResponse
from app.repositories.protocols.users_repository_protocol import UsersRepository

security_router = APIRouter()


@security_router.get("/me", response_model=UserResponse)
async def me(
    user_id: int = Depends(get_current_user_id),
    user_repo: UsersRepository = Depends(get_inmemory_users_repo),
):
    user = await user_repo.get_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(email=user.email, name=user.name, role=user.role)
