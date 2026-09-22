from fastapi import APIRouter, Depends

from app.dependencies import get_change_user_role_uc
from app.entities.user_entity import UserEntity, UserRole
from app.use_cases.change_user_role import ChangeUserRoleUseCase

change_user_router = APIRouter()


@change_user_router.post("/change/role")
async def change_role(
    user_id: int,
    new_role: UserRole,
    change_user_role_uc: ChangeUserRoleUseCase = Depends(get_change_user_role_uc),
) -> UserEntity:
    return await change_user_role_uc.execute(user_id=user_id, new_role=new_role)
