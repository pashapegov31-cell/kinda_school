from datetime import datetime, timezone

from app.entities.user_entity import UserEntity
from app.models.user_model import UserCreate
from app.repositories.inmemory.inmemory_users_repository import InMemoryUsersRepository

session = InMemoryUsersRepository()
user_id = -1


async def registrate_user(session, user_data: UserCreate) -> UserEntity:
    await session.add_email(user_data.email)
    global user_id
    user_id += 1
    new_user = UserEntity(
        id=user_id,
        email=user_data.email,
        name=user_data.name,
        hashed_password=user_data.password,
        created_at=datetime.now(tz=timezone.utc),
    )
    await session.create(new_user)
    return new_user
