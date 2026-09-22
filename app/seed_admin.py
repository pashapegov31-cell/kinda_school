from datetime import datetime, timezone

from app.core.config_settings import settings
from app.dependencies import users_repo
from app.entities.user_entity import UserEntity, UserRole
from app.utils.passlib_hash import hash_password


async def seed_admin():
    if await users_repo.exists_email(settings.ADMIN_EMAIL):
        return
    admin = UserEntity(
        id=0,
        email=settings.ADMIN_EMAIL,
        name=settings.ADMIN_NAME,
        role=UserRole.ADMIN,
        hashed_password=await hash_password(settings.ADMIN_PASSWORD),
        created_at=datetime.now(tz=timezone.utc),
    )
    await users_repo.create(admin)
