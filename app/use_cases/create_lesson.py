from app.entities.lesson_entity import LessonEntity
from app.exceptions.exceptions import ForbiddenError, NotFoundError
from app.models.lesson_model import LessonCreate
from app.repositories.protocols.course_repository_protocol import CourseRepository
from app.repositories.protocols.lesson_repository_protocol import LessonRepository


class LessonCreateUseCase:
    def __init__(self, lessons_repo: LessonRepository, courses_repo: CourseRepository):
        self._lessons_repo = lessons_repo
        self._courses_repo = courses_repo

    async def execute(
        self,
        after_lesson_id: int,
        lesson: LessonCreate,
        course_id: int,
        teacher_id: int,
    ) -> LessonEntity:
        course = await self._courses_repo.get_by_id(course_id)
        if not course:
            raise NotFoundError("Такого курса не существует")
        if course.teacher_id != teacher_id:
            raise ForbiddenError("Вы не являтесь владельцем данного курса")
        lessons = await self._lessons_repo.get_by_course_id(course_id)
        after_lesson = next(
            (lesson for lesson in lessons if lesson.id == after_lesson_id), None
        )
        if after_lesson is None:
            raise NotFoundError("Урок не найден в этом курсе")
        order = after_lesson.order + 1
        for l in lessons[order - 1 :]:
            l.order += 1
            await self._lessons_repo.update(l)
        new_lesson = LessonEntity(
            id=0,
            course_id=course_id,
            title=lesson.title,
            content=lesson.content,
            video_url=lesson.video_url,
            order=order,
            duration_minutes=0,
        )
        return await self._lessons_repo.create(new_lesson)
