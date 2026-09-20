from app.entities.user_entity import UserEntity


class InMemoryUsersRepository:
    def __init__(self):
        self._users: dict[int, UserEntity] = {}
        self._next_id = 0

    async def get_by_email(self, email: str) -> UserEntity | None:
        for user in self._users.values():
            if user.email == email:
                return user
        return None

    async def get_by_id(self, user_id: int) -> UserEntity | None:
        return self._users.get(user_id)

    async def get_by_name(self, name: str) -> UserEntity | None:
        for user in self._users.values():
            if name == user.name:
                return user
        return None

    async def create(self, new_user: UserEntity) -> UserEntity:
        new_user.id = self._next_id
        self._users[new_user.id] = new_user
        self._next_id += 1

        return new_user

    async def exists_email(self, email: str) -> bool:
        for user in self._users.values():
            if user.email == email:
                return True
        return False
