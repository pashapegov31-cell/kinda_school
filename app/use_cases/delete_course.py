from app.entities.user_entity import UserRole
from app.exceptions.exceptions import ForbiddenError, NotFoundError
from app.repositories.protocols.course_repository_protocol import CourseRepository
from app.repositories.protocols.enrollment_repository_protocol import (
    EnrollmentRepository,
)
from app.repositories.protocols.lesson_progress_repository_protocol import (
    LessonProgressRepository,
)
from app.repositories.protocols.lesson_repository_protocol import LessonRepository
from app.repositories.protocols.users_repository_protocol import UsersRepository


class DeleteCourseUseCase:
    def __init__(
        self,
        courses_repo: CourseRepository,
        users_repo: UsersRepository,
        lessons_repo: LessonRepository,
        lesson_progress_repo: LessonProgressRepository,
        enrollments_repo: EnrollmentRepository,
    ):
        self._courses_repo = courses_repo
        self._users_repo = users_repo
        self._lessons_repo = lessons_repo
        self._lesson_progress_repo = lesson_progress_repo
        self._enrollments_repo = enrollments_repo

    async def execute(self, course_id: int, teacher_id: int):
        teacher = await self._users_repo.get_by_id(teacher_id)
        if not teacher:
            raise NotFoundError("Пользователь с таким айди не найден")
        course = await self._courses_repo.get_by_id(course_id)
        if not course:
            raise NotFoundError("Курс не найден")
        if course.teacher_id != teacher_id and teacher.role != UserRole.ADMIN:
            raise ForbiddenError("Нельзя удалять чужой курс")

        lessons = await self._lessons_repo.get_by_course_id(course_id)
        for lesson in lessons:
            await self._lessons_repo.delete(lesson.id)
        enrollments = await self._enrollments_repo.get_by_course_id(course_id)
        for enrollment in enrollments:
            enrollment_id = enrollment.id
            lesson_progresses = await self._lesson_progress_repo.get_by_enrollment_id(
                enrollment_id
            )
            for lesson_progress in lesson_progresses:
                await self._lesson_progress_repo.delete(lesson_progress.id)
            await self._enrollments_repo.delete(enrollment_id)
        await self._courses_repo.delete(course_id)
