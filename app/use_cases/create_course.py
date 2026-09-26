from datetime import datetime, timezone

from app.entities.course_entity import CourseEntity, CourseStatus
from app.entities.lesson_entity import LessonEntity
from app.exceptions.exceptions import NotValidPrice
from app.models.course_model import CourseCreate
from app.repositories.protocols.course_repository_protocol import CourseRepository
from app.repositories.protocols.lesson_repository_protocol import LessonRepository


class CreateCourseUseCase:
    def __init__(self, course_repo: CourseRepository, lessons_repo: LessonRepository):
        self._course_repo = course_repo
        self._lessons_repo = lessons_repo

    async def execute(self, new_course: CourseCreate, teacher_id: int) -> CourseEntity:
        if new_course.price < 0:
            raise NotValidPrice("Цена не может бфть отрицательной")

        now = datetime.now(tz=timezone.utc)
        course = CourseEntity(
            id=0,
            teacher_id=teacher_id,
            title=new_course.title,
            description=new_course.description,
            price=new_course.price,
            status=CourseStatus.DRAFT,
            created_at=now,
            updated_at=now,
        )
        created_course = await self._course_repo.create(course)
        base_lesson = LessonEntity(
            id=0,
            course_id=created_course.id,
            title="Это мой первый урок в данном курсе",
            content="Здесь будет контент",
            video_url=None,
            order=1,
            duration_minutes=0,
        )
        await self._lessons_repo.create(base_lesson)
        return created_course
