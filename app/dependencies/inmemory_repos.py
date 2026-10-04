from app.repositories.inmemory.inmemory_courses_repository import (
    InMemoryCourseRepository,
)
from app.repositories.inmemory.inmemory_enrollments_repository import (
    InMemoryEnrollmentRepository,
)
from app.repositories.inmemory.inmemory_lesson_progresses_repository import (
    InMemoryLessonProgressRepository,
)
from app.repositories.inmemory.inmemory_lessons_repository import (
    InMemoryLessonRepository,
)
from app.repositories.inmemory.inmemory_users_repository import InMemoryUsersRepository

users_repo = InMemoryUsersRepository()
courses_repo = InMemoryCourseRepository()
lessons_repo = InMemoryLessonRepository()
enrollments_repo = InMemoryEnrollmentRepository()
lessons_progress_repo = InMemoryLessonProgressRepository()


def get_users_repo():
    return users_repo


def get_courses_repo():
    return courses_repo


def get_lessons_repo():
    return lessons_repo


def get_enrollments_repo():
    return enrollments_repo


def get_lessons_progress_repo():
    return lessons_progress_repo
