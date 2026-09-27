from app.entities.course_entity import CourseStatus
from app.entities.lesson_entity import LessonEntity
from app.exceptions.exceptions import ForbiddenError, NotFoundError
from app.repositories.protocols.course_repository_protocol import CourseRepository
from app.repositories.protocols.enrollment_repository_protocol import (
    EnrollmentRepository,
)
from app.repositories.protocols.lesson_repository_protocol import LessonRepository


class GetLessonDetailsUseCase:
    def __init__(
        self,
        lessons_repo: LessonRepository,
        courses_repo: CourseRepository,
        enrollments_repo: EnrollmentRepository,
    ):
        self._lessons_repo = lessons_repo
        self._courses_repo = courses_repo
        self._enrollments_repo = enrollments_repo

    async def execute(
        self, course_id: int, lesson_id: int, user_id: int
    ) -> LessonEntity:
        lesson = await self._lessons_repo.get_by_id(lesson_id)
        course = await self._courses_repo.get_by_id(course_id)
        if not course:
            raise NotFoundError("Курс не найден")
        if not lesson or lesson.course_id != course_id:
            raise NotFoundError("Урок не найден")
        if course.teacher_id != user_id:
            if course.status != CourseStatus.PUBLISHED:
                raise NotFoundError("Курс не найден")
            enrollment = await self._enrollments_repo.get_by_user_and_course(
                user_id, course_id
            )
            if not enrollment:
                raise ForbiddenError(
                    "Запишитесь на курс для просмотра содержимого уроков"
                )
        return lesson
