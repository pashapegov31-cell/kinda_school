from app.entities.course_entity import CourseStatus
from app.exceptions.exceptions import NotFoundError
from app.repositories.protocols.course_repository_protocol import CourseRepository
from app.repositories.protocols.lesson_repository_protocol import LessonRepository


class GetCourseLessonsList:
    def __init__(self, courses_repo: CourseRepository, lessons_repo: LessonRepository):
        self._courses_repo = courses_repo
        self._lessons_repo = lessons_repo

    async def execute(self, course_id: int, teacher_id: int) -> list:
        course = await self._courses_repo.get_by_id(course_id)
        if not course:
            raise NotFoundError("Курс не найден")
        if course.status != CourseStatus.PUBLISHED and course.teacher_id != teacher_id:
            raise NotFoundError("Курс не найден")

        lessons = await self._lessons_repo.get_by_course_id(course_id)
        return lessons
