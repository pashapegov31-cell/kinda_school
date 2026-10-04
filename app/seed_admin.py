from datetime import datetime, timezone

from app.core.config_settings import settings
from app.core.database import async_session_factory
from app.entities.user_entity import UserEntity, UserRole
from app.repositories.protocols.users_repository_protocol import UsersRepository
from app.utils.passlib_hash import hash_password


async def _seed_admin_if_absent(repo: UsersRepository) -> None:
    if await repo.exists_email(settings.ADMIN_EMAIL):
        return
    admin = UserEntity(
        id=0,
        email=settings.ADMIN_EMAIL,
        name=settings.ADMIN_NAME,
        role=UserRole.ADMIN,
        hashed_password=await hash_password(settings.ADMIN_PASSWORD),
        created_at=datetime.now(tz=timezone.utc),
    )
    await repo.create(admin)


async def seed_admin():
    if settings.BACKEND_REPO == "postgres":
        from app.repositories.postgres.pg_users_repo import SQLUsersRepository

        async with async_session_factory() as session:
            await _seed_admin_if_absent(SQLUsersRepository(session))
            await session.commit()

    else:
        from app.dependencies.switch_repos import users_repo

        await _seed_admin_if_absent(users_repo)
