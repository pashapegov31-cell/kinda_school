# from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.routes.auth_route import auth_router
from app.routes.course_route import course_router
from app.routes.security_route import security_router

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

app.include_router(auth_router, prefix="/v1", tags=["Auth"])
app.include_router(security_router, prefix="/v1", tags=["Me"])
app.include_router(course_router, prefix="/v1", tags=["Courses"])
