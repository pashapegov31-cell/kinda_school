from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.repositories.postgres.pg_courses_repo import (
    SQLCourseRepository,
)
from app.repositories.postgres.pg_enrollments_repo import (
    SQLEnrollmentRepository,
)
from app.repositories.postgres.pg_lesson_progresses_repo import (
    SQLLessonProgressesRepository,
)
from app.repositories.postgres.pg_lessons_repo import (
    SQLLessonsRepository,
)
from app.repositories.postgres.pg_users_repo import SQLUsersRepository


def get_users_repo(session: AsyncSession = Depends(get_session)):
    return SQLUsersRepository(session)


def get_courses_repo(session: AsyncSession = Depends(get_session)):
    return SQLCourseRepository(session)


def get_lessons_repo(session: AsyncSession = Depends(get_session)):
    return SQLLessonsRepository(session)


def get_enrollments_repo(session: AsyncSession = Depends(get_session)):
    return SQLEnrollmentRepository(session)


def get_lessons_progress_repo(session: AsyncSession = Depends(get_session)):
    return SQLLessonProgressesRepository(session)
