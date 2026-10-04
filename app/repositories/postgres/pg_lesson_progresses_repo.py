from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.lesson_progress_entity import LessonProgressEntity
from app.exceptions.exceptions import CantBeUpdatedError
from app.repositories.protocols.lesson_progress_repository_protocol import (
    LessonProgressRepository,
)
from app.schemas.pg_lesson_progress_schema import LessonProgress


class SQLLessonProgressesRepository(LessonProgressRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    @staticmethod
    def _to_entity(row: LessonProgress) -> LessonProgressEntity:
        lesson_progress = LessonProgressEntity(
            id=row.id,
            enrollment_id=row.enrollment_id,
            lesson_id=row.lesson_id,
            completed=row.completed,
            completed_at=row.completed_at,
        )
        return lesson_progress

    async def create(
        self, lesson_progress: LessonProgressEntity
    ) -> LessonProgressEntity:
        row = LessonProgress(
            enrollment_id=lesson_progress.enrollment_id,
            lesson_id=lesson_progress.lesson_id,
            completed=lesson_progress.completed,
            completed_at=lesson_progress.completed_at,
        )
        self._session.add(row)
        await self._session.flush()
        return self._to_entity(row)

    async def get_by_id(self, lesson_progress_id: int) -> LessonProgressEntity | None:
        row = await self._session.get(LessonProgress, lesson_progress_id)
        if not row:
            return None
        return self._to_entity(row)

    async def get_by_enrollment_and_lesson(
        self, enrollment_id: int, lesson_id: int
    ) -> LessonProgressEntity | None:
        lesson_pr = await self._session.execute(
            select(LessonProgress).where(
                LessonProgress.enrollment_id == enrollment_id,
                LessonProgress.lesson_id == lesson_id,
            )
        )
        row = lesson_pr.scalar_one_or_none()
        if not row:
            return None
        return self._to_entity(row)

    async def get_by_enrollment_id(
        self, enrollment_id: int
    ) -> list[LessonProgressEntity]:
        lesson_prs = await self._session.execute(
            select(LessonProgress)
            .where(LessonProgress.enrollment_id == enrollment_id)
            .order_by(LessonProgress.id)
        )
        rows = lesson_prs.scalars()
        return [self._to_entity(l) for l in rows]

    async def get_by_lesson_id(self, lesson_id: int) -> list[LessonProgressEntity]:
        lesson_prs = await self._session.execute(
            select(LessonProgress)
            .where(LessonProgress.lesson_id == lesson_id)
            .order_by(LessonProgress.id)
        )
        rows = lesson_prs.scalars()
        return [self._to_entity(l) for l in rows]

    async def update(
        self, lesson_progress: LessonProgressEntity
    ) -> LessonProgressEntity:
        lesson_pr = await self._session.get(LessonProgress, lesson_progress.id)
        if not lesson_pr:
            raise CantBeUpdatedError("Нельзя изменить несуществующий прогресс")
        lesson_pr.completed_at = lesson_progress.completed_at
        lesson_pr.completed = lesson_progress.completed
        await self._session.flush()
        return self._to_entity(lesson_pr)

    async def delete(self, lesson_progress_id: int) -> None:
        lesson_pr = await self._session.get(LessonProgress, lesson_progress_id)
        if not lesson_pr:
            return
        await self._session.delete(lesson_pr)
        await self._session.flush()
