from app.entities.user_entity import UserRole
from app.exceptions.exceptions import CantBeUpdatedError
from app.repositories.protocols.users_repository_protocol import UsersRepository


class ChangeUserRoleUseCase:
    def __init__(self, user_repo: UsersRepository):
        self._user_repo = user_repo

    async def execute(self, user_id: int, new_role: UserRole):
        user = await self._user_repo.get_by_id(user_id)
        if not user:
            raise CantBeUpdatedError("Пользователя не существует")
        user.role = new_role
        return user
