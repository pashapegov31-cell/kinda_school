from fastapi import APIRouter, Depends

from app.dependencies import get_change_user_role_uc, require_role
from app.entities.user_entity import UserRole
from app.models.user_model import ChangeUserRole, UserResponse
from app.use_cases.change_user_role import ChangeUserRoleUseCase

user_router = APIRouter()


@user_router.post("/change/role", response_model=UserResponse)
async def change_role(
    change_role: ChangeUserRole,
    admin_id: int = Depends(require_role(role=UserRole.ADMIN)),
    change_user_role_uc: ChangeUserRoleUseCase = Depends(get_change_user_role_uc),
):
    updated_user = await change_user_role_uc.execute(change_role=change_role)
    return UserResponse(
        email=updated_user.email, name=updated_user.name, role=updated_user.role
    )
