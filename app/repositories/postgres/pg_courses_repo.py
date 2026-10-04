from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.course_entity import CourseEntity, CourseStatus
from app.exceptions.exceptions import CantBeUpdatedError
from app.repositories.protocols.course_repository_protocol import CourseRepository
from app.schemas.pg_courses_schema import Course


class SQLCourseRepository(CourseRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    @staticmethod
    def _to_entity(row: Course) -> CourseEntity:
        course = CourseEntity(
            id=row.id,
            teacher_id=row.teacher_id,
            title=row.title,
            description=row.description,
            price=row.price,
            status=row.status,
            created_at=row.created_at,
            updated_at=row.updated_at,
        )
        return course

    async def create(self, course: CourseEntity) -> CourseEntity:
        new_course = Course(
            teacher_id=course.teacher_id,
            title=course.title,
            description=course.description,
            price=course.price,
            status=course.status,
            created_at=course.created_at,
            updated_at=course.updated_at,
        )
        self._session.add(new_course)
        await self._session.flush()
        return self._to_entity(new_course)

    async def get_all_courses(self) -> list[CourseEntity]:
        courses = await self._session.execute(select(Course).order_by(Course.id))
        rows = courses.scalars()
        return [self._to_entity(c) for c in rows]

    async def get_by_id(self, course_id: int) -> CourseEntity | None:
        row = await self._session.get(Course, course_id)
        if not row:
            return None
        return self._to_entity(row)

    async def get_by_teacher_id(self, teacher_id: int) -> list[CourseEntity]:
        courses = await self._session.execute(
            select(Course).where(Course.teacher_id == teacher_id).order_by(Course.id)
        )
        rows = courses.scalars()
        return [self._to_entity(c) for c in rows]

    async def get_published(self) -> list[CourseEntity]:
        courses = await self._session.execute(
            select(Course)
            .where(Course.status == CourseStatus.PUBLISHED)
            .order_by(Course.id)
        )
        rows = courses.scalars()
        return [self._to_entity(c) for c in rows]

    async def delete(self, course_id: int) -> None:
        course = await self._session.get(Course, course_id)
        if not course:
            return
        await self._session.delete(course)
        await self._session.flush()

    async def update(self, course: CourseEntity) -> CourseEntity:
        cours = await self._session.get(Course, course.id)
        if not cours:
            raise CantBeUpdatedError("Нельзя изменить несуществующий курс")
        cours.status = course.status
        cours.description = course.description
        cours.price = course.price
        cours.title = course.title
        cours.updated_at = datetime.now(tz=timezone.utc)
        await self._session.flush()
        return self._to_entity(cours)
