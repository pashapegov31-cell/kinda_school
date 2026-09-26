from app.entities.course_entity import CourseEntity, CourseStatus
from app.exceptions.exceptions import CantBeUpdatedError, ForbiddenError
from app.repositories.protocols.course_repository_protocol import CourseRepository


class PublishCourseUseCase:
    def __init__(self, courses_repo: CourseRepository):
        self._courses_repo = courses_repo

    async def execute(self, course_id: int, teacher_id: int) -> CourseEntity:
        course = await self._courses_repo.get_by_id(course_id)
        if not course:
            raise CantBeUpdatedError("Нельзя опубликовать несуществующий курс")
        if course.teacher_id != teacher_id:
            raise ForbiddenError("Недостаточно прав на данное действие")
        if course.status == CourseStatus.PUBLISHED:
            raise CantBeUpdatedError("Курс уже опубликован")
        course.status = CourseStatus.PUBLISHED
        return await self._courses_repo.update(course)
