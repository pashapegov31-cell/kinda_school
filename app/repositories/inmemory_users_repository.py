from app.entities.user_entity import UserEntity


class InMemoryUsersRepository:
    user_id = -1

    def __init__(self):
        self._users: dict[int, UserEntity] = {}
        self.user_id += 1

    def get_by_email(self, email: str) -> UserEntity | None:
        for user in self._users.values():
            if email == user.email:
                return user
        return None

    def get_by_id(self, id: int) -> UserEntity | None:
        return self._users[id] or None

    def get_by_name(self, name: str) -> UserEntity | None:
        for user in self._users.values():
            if name == user.name:
                return user
        return None

    def create(self, new_user: UserEntity) -> UserEntity:
        self._users[new_user.id] = new_user
        return new_user
