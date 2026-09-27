from datetime import datetime, timezone

from app.entities.course_entity import CourseStatus
from app.entities.enrollment_entity import EnrollmentEntity
from app.entities.user_entity import UserRole
from app.exceptions.exceptions import ForbiddenError, NotFoundError
from app.repositories.protocols.course_repository_protocol import CourseRepository
from app.repositories.protocols.enrollment_repository_protocol import (
    EnrollmentRepository,
)
from app.repositories.protocols.users_repository_protocol import UsersRepository


class EnrollInCourseUseCase:
    def __init__(
        self,
        enrollments_repo: EnrollmentRepository,
        courses_repo: CourseRepository,
        users_repo: UsersRepository,
    ):
        self._enrollments_repo = enrollments_repo
        self._courses_repo = courses_repo
        self._users_repo = users_repo

    async def execute(self, user_id: int, course_id: int) -> EnrollmentEntity:
        user = await self._users_repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("Пользователь не найден")
        if user.role != UserRole.STUDENT:
            raise ForbiddenError("Пользователь не является студентом")
        if await self._enrollments_repo.get_by_user_and_course(user_id, course_id):
            raise ForbiddenError("Вы уже записаны на этот курс")
        course = await self._courses_repo.get_by_id(course_id)
        if not course or course.status != CourseStatus.PUBLISHED:
            raise NotFoundError("Курс не найден")
        if course.teacher_id == user_id:
            raise ForbiddenError("Нельзя записаться на свой собственный курс")
        now = datetime.now(timezone.utc)
        enrollment = EnrollmentEntity(
            id=0,
            user_id=user.id,
            course_id=course.id,
            enrolled_at=now,
            progress=0,
            completed=False,
            completed_at=None,
            updated_at=now,
        )
        enrollment = await self._enrollments_repo.create(enrollment)
        return enrollment
