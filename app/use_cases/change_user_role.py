from app.entities.user_entity import UserEntity
from app.exceptions.exceptions import NoSuchUser
from app.models.user_model import ChangeUserRole
from app.repositories.protocols.users_repository_protocol import UsersRepository


class ChangeUserRoleUseCase:
    def __init__(self, user_repo: UsersRepository):
        self._user_repo = user_repo

    async def execute(self, change_role: ChangeUserRole) -> UserEntity:
        user = await self._user_repo.get_by_id(change_role.user_id)
        if not user:
            raise NoSuchUser("Такого пользователя не существует")
        user.role = change_role.new_role
        user = await self._user_repo.update(user)
        return user
