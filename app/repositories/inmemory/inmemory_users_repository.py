from app.entities.user_entity import UserEntity


class InMemoryUsersRepository:
    def __init__(self):
        self._users: dict[int, UserEntity] = {}
        self.__emails: list[str] = []

    async def get_by_email(self, email: str) -> UserEntity | None:
        if not self.check_email(email, await self.get_all_emails()):
            return None
        for user in self._users.values():
            if user.email == email:
                return user
        raise Exception("какая-то ошибка")

    async def get_by_id(self, id: int) -> UserEntity | None:
        return self._users[id] or None

    async def get_by_name(self, name: str) -> UserEntity | None:
        for user in self._users.values():
            if name == user.name:
                return user
        return None

    async def create(self, new_user: UserEntity) -> UserEntity:
        self._users[new_user.id] = new_user

        return new_user

    async def get_all_emails(self) -> list[str]:
        return self.__emails

    async def add_email(self, email: str) -> None:
        if await self.check_email(email, await self.get_all_emails()):
            self.__emails.append(email)
            return
        raise Exception("Пользователь с данным email уже существует")

    @staticmethod
    async def check_email(email: str, emails: list[str]) -> bool:
        return email not in emails
