from app.exceptions.exceptions import NotFoundError
from app.repositories.protocols.course_repository_protocol import CourseRepository
from app.repositories.protocols.lesson_repository_protocol import LessonRepository


class GetCourseLessonsList:
    def __init__(self, courses_repo: CourseRepository, lessons_repo: LessonRepository):
        self._courses_repo = courses_repo
        self._lessons_repo = lessons_repo

    async def execute(self, course_id: int):
        lessons = await self._lessons_repo.get_by_course_id(course_id)
        if not lessons:
            raise NotFoundError("Такого курса нет в каталоге")
        return lessons
