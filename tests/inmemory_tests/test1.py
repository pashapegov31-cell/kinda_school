import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import asyncio

from app.models.user_model import UserCreate
from app.repositories.inmemory.inmemory_users_repository import InMemoryUsersRepository
from app.use_cases.registrate_user import registrate_user

i = 0
user_repo = InMemoryUsersRepository()
pasha = UserCreate(
    email="pashapegov31@gmail.com", name="Pasha Pegov", password="pashapegov2007"
)

nastya = UserCreate(
    email="yamopsikgavgav@gmail.com", name="Nastay Chekanova", password="Алиса"
)


async def main():
    await registrate_user(user_repo, pasha)
    await registrate_user(user_repo, nastya)
    await registrate_user(user_repo, nastya)
    #     print(await user_repo.get_by_email("pashapegov31@gmail.com"))
    print(await user_repo.get_all_emails())


if __name__ == "__main__":
    asyncio.run(main())
