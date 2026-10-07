from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.user_entity import UserEntity
from app.exceptions.exceptions import CantBeUpdatedError
from app.repositories.protocols.users_repository_protocol import UsersRepository
from app.schemas.pg_users_schema import User


class SQLUsersRepository(UsersRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    @staticmethod
    def _to_entity(row: User) -> UserEntity:
        return UserEntity(
            id=row.id,
            email=row.email,
            name=row.name,
            role=row.role,
            hashed_password=row.hashed_password,
            created_at=row.created_at,
        )

    async def get_by_email(self, email: str) -> UserEntity | None:
        user = await self._session.execute(select(User).where(User.email == email))
        row = user.scalar_one_or_none()
        if not row:
            return None
        return self._to_entity(row)

    async def get_by_id(self, user_id: int) -> UserEntity | None:
        row = await self._session.get(User, user_id)
        if not row:
            return None
        return self._to_entity(row)

    async def get_by_name(self, name: str) -> UserEntity | None:
        user = await self._session.execute(select(User).where(User.name == name))
        row = user.scalar_one_or_none()
        if not row:
            return None
        return self._to_entity(row)

    async def create(self, new_user: UserEntity) -> UserEntity:
        row = User(
            email=new_user.email,
            name=new_user.name,
            role=new_user.role,
            hashed_password=new_user.hashed_password,
            created_at=new_user.created_at,
        )
        self._session.add(row)
        await self._session.flush()
        return self._to_entity(row)

    async def exists_email(self, email: str) -> bool:
        em = await self._session.execute(select(User.id).where(User.email == email))
        return em.first() is not None

    async def update(self, updated_user: UserEntity) -> UserEntity:
        row = await self._session.get(User, updated_user.id)
        if not row:
            raise CantBeUpdatedError("Нельзя изменить несуществующего пользователя")
        row.name = updated_user.name
        row.role = updated_user.role
        row.hashed_password = updated_user.hashed_password
        await self._session.flush()
        return self._to_entity(row)

    async def get_users(self, offset: int, limit: int) -> list[UserEntity]:
        users = await self._session.execute(
            select(User).where(User.id > offset, User.id <= offset + limit)
        )
        rows = users.scalars()
        return [self._to_entity(u) for u in rows]
