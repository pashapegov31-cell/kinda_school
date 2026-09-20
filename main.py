# from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI

from app.dependencies import get_inmemory_user_repo, get_register_uc
from app.models.user_model import AuthResponse, UserCreate
from app.services.auth_service import AuthService

# from redis.asyncio import ConnectionPool, Redis


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     app.state.redis_pool = ConnectionPool(
#         host="localhost",
#         db=0,
#         port=6379,
#         max_connections=10,
#         protocol=2,
#         decode_responses=True,
#     )

#     app.state.redis = Redis(connection_pool=app.state.redis_pool)

#     yield

#     await app.state.redis.close()
#     await app.state.redis_pool.disconnect()


app = FastAPI()


@app.post("/v1/register")
async def register(
    email: str,
    name: str,
    password: str,
    user_repo=Depends(get_inmemory_user_repo),
    register_uc=Depends(get_register_uc),
) -> AuthResponse | None:
    new_user = UserCreate(email=email, name=name, password=password)
    await AuthService(user_repo, register_uc, login_uc=None).register(new_user)
