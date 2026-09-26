from app.entities.course_entity import CourseStatus
from app.entities.lesson_entity import LessonEntity
from app.exceptions.exceptions import ForbiddenError, NotFoundError
from app.repositories.protocols.course_repository_protocol import CourseRepository
from app.repositories.protocols.lesson_repository_protocol import LessonRepository


class GetLessonDetailsUseCase:
    def __init__(self, lessons_repo: LessonRepository, courses_repo: CourseRepository):
        self._lesssons_repo = lessons_repo
        self._courses_repo = courses_repo

    async def execute(
        self, course_id: int, lesson_id: int, teacher_id: int
    ) -> LessonEntity:
        lesson = await self._lesssons_repo.get_by_id(lesson_id)
        course = await self._courses_repo.get_by_id(course_id)
        if not course:
            raise NotFoundError("Курс не найден")
        if not lesson or lesson.course_id != course_id:
            raise NotFoundError("Урок не найден")
        if course.status != CourseStatus.PUBLISHED:
            if course.teacher_id != teacher_id:
                raise ForbiddenError(
                    "Недостаточно прав для просмотра содержимого урока"
                )
        return LessonEntity(
            id=lesson.id,
            course_id=course_id,
            title=lesson.title,
            content=lesson.content,
            video_url=lesson.video_url,
            order=lesson.order,
            duration_minutes=lesson.duration_minutes,
        )
