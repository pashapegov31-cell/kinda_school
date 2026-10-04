from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.lesson_entity import LessonEntity
from app.exceptions.exceptions import CantBeUpdatedError
from app.repositories.protocols.lesson_repository_protocol import LessonRepository
from app.schemas.pg_lessons_schema import Lesson


class SQLLessonsRepository(LessonRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    @staticmethod
    def _to_entity(row: Lesson) -> LessonEntity:
        lesson = LessonEntity(
            id=row.id,
            course_id=row.course_id,
            title=row.title,
            content=row.content,
            video_url=row.video_url,
            order=row.order,
            duration_minutes=row.duration_minutes,
        )
        return lesson

    async def create(self, lesson: LessonEntity) -> LessonEntity:
        row = Lesson(
            course_id=lesson.course_id,
            title=lesson.title,
            content=lesson.content,
            video_url=lesson.video_url,
            order=lesson.order,
            duration_minutes=lesson.duration_minutes,
        )
        self._session.add(row)
        await self._session.flush()
        return self._to_entity(row)

    async def get_by_id(self, lesson_id: int) -> LessonEntity | None:
        row = await self._session.get(Lesson, lesson_id)
        if not row:
            return None
        return self._to_entity(row)

    async def get_by_course_id(self, course_id: int) -> list[LessonEntity]:
        leses = await self._session.execute(
            select(Lesson).where(Lesson.course_id == course_id).order_by(Lesson.order)
        )
        rows = leses.scalars()
        return [self._to_entity(l) for l in rows]

    async def update(self, lesson: LessonEntity) -> LessonEntity:
        les = await self._session.get(Lesson, lesson.id)
        if not les:
            raise CantBeUpdatedError("Нельзя изменить несуществующий урок")
        les.duration_minutes = lesson.duration_minutes
        les.order = lesson.order
        les.video_url = lesson.video_url
        les.content = lesson.content
        les.title = lesson.title
        await self._session.flush()
        return self._to_entity(les)

    async def delete(self, lesson_id: int) -> None:
        les = await self._session.get(Lesson, lesson_id)
        if not les:
            return
        await self._session.delete(les)
        await self._session.flush()
