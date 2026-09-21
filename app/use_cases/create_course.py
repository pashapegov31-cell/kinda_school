from datetime import datetime, timezone

from app.entities.course_entity import CourseEntity, CourseStatus
from app.exceptions.exceptions import NotValidPrice
from app.models.course_model import CourseCreate
from app.repositories.protocols.course_repository_protocol import CourseRepository


class CreateCourseUseCase:
    def __init__(self, course_repo: CourseRepository):
        self._course_repo = course_repo

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
        return await self._course_repo.create(course)
