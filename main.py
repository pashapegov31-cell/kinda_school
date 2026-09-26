from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions.exceptions import (
    AuthError,
    ForbiddenError,
    NotFoundError,
    TokenError,
    UserAlreadyExistsError,
    UserError,
)
from app.routes.auth_route import auth_router
from app.routes.course_route import course_router
from app.routes.lesson_router import lesson_router
from app.routes.security_route import security_router
from app.routes.user_route import user_router
from app.seed_admin import seed_admin


@asynccontextmanager
async def lifespan(app: FastAPI):
    await seed_admin()

    yield


app = FastAPI(lifespan=lifespan)


@app.exception_handler(ForbiddenError)
async def forbidden_handler(request: Request, exc: ForbiddenError):
    return JSONResponse(status_code=403, content={"detail": str(exc)})


@app.exception_handler(AuthError)
async def auth_handler(request: Request, exc: AuthError):
    return JSONResponse(status_code=401, content={"detail": str(exc)})


@app.exception_handler(TokenError)
async def token_handler(request: Request, exc: TokenError):
    return JSONResponse(status_code=401, content={"detail": str(exc)})


@app.exception_handler(UserError)
async def user_handler(request: Request, exc: UserError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(UserAlreadyExistsError)
async def user_exists_handler(request: Request, exc: UserAlreadyExistsError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})


@app.exception_handler(NotFoundError)
async def update_hadler(request: Request, exc: NotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


app.include_router(auth_router, prefix="/v1", tags=["Auth"])
app.include_router(security_router, prefix="/v1", tags=["Me"])
app.include_router(course_router, prefix="/v1", tags=["Courses"])
app.include_router(user_router, prefix="/v1", tags=["Users"])
app.include_router(lesson_router, prefix="/v1", tags=["Lessons"])
