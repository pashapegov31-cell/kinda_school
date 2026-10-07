from fastapi import APIRouter, Depends, Query

from app.dependencies.auth_dependencies import require_role
from app.dependencies.switch_repos import get_users_repo
from app.dependencies.use_cases_dependencies import get_change_user_role_uc
from app.entities.user_entity import UserRole
from app.models.user_model import ChangeUserRole, UserResponse
from app.repositories.protocols.users_repository_protocol import UsersRepository
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


@user_router.get("/users", response_model=list[UserResponse])
async def get_users(
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    users_repo: UsersRepository = Depends(get_users_repo),
    admin=Depends(require_role(UserRole.ADMIN)),
):
    users = await users_repo.get_users(offset, limit)
    return [
        UserResponse.model_validate(user) for user in users[offset : offset + limit]
    ]
