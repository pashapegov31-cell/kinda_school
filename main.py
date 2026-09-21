from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.routes.auth_route import auth_router
from app.routes.course_route import course_router
from app.routes.security_route import security_router
from app.seed_admin import seed_admin


@asynccontextmanager
async def lifespan(app: FastAPI):
    await seed_admin()

    yield


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router, prefix="/v1", tags=["Auth"])
app.include_router(security_router, prefix="/v1", tags=["Me"])
app.include_router(course_router, prefix="/v1", tags=["Courses"])
