from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config_settings import settings
from app.dependencies.switch_repos import get_users_repo
from app.entities.user_entity import UserRole
from app.exceptions.exceptions import TokenError
from app.repositories.protocols.users_repository_protocol import UsersRepository
from app.services.token_service import TokenService

bearer = HTTPBearer()
token_service = TokenService(settings.TOKEN_SECRET_KEY, settings.ALGORITHM)


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
) -> int:
    token = credentials.credentials
    try:
        return token_service.verify_access_token(token)
    except TokenError as e:
        raise HTTPException(
            status_code=401, detail=str(e), headers={"WWW-Authenticate": "Bearer"}
        )


def require_role(role: UserRole):
    async def check(
        user_id: int = Depends(get_current_user_id),
        user_repo: UsersRepository = Depends(get_users_repo),
    ) -> int:
        user = await user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User Not Found")
        if user.role not in [role, UserRole.ADMIN]:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user_id

    return check
