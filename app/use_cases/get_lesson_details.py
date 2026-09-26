from app.exceptions.exceptions import ForbiddenError, NotFoundError
from app.models.lesson_model import LessonResponse
from app.repositories.protocols.lesson_repository_protocol import LessonRepository


class GetLessonDetailsUseCase:
    def __init__(self, lessons_repo: LessonRepository):
        self._lesssons_repo = lessons_repo

    async def execute(self, course_id: int, lesson_id: int) -> LessonResponse:
        lesson = await self._lesssons_repo.get_by_id(lesson_id)
        if not lesson:
            raise NotFoundError("Такого урока не существует")
        if lesson.course_id != course_id:
            raise ForbiddenError("Такого урока нет в данном курсе")
        return LessonResponse(
            id=lesson.id,
            course_id=course_id,
            title=lesson.title,
            content=lesson.content,
            video_url=lesson.video_url,
            order=lesson.order,
            duration_minutes=lesson.duration_minutes,
        )
