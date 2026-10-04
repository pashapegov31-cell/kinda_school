from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.enrollment_entity import EnrollmentEntity
from app.exceptions.exceptions import CantBeUpdatedError
from app.repositories.protocols.enrollment_repository_protocol import (
    EnrollmentRepository,
)
from app.schemas.pg_enrollments_schema import Enrollment


class SQLEnrollmentRepository(EnrollmentRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    @staticmethod
    def _to_entity(row: Enrollment) -> EnrollmentEntity:
        enrollment = EnrollmentEntity(
            id=row.id,
            user_id=row.user_id,
            course_id=row.course_id,
            enrolled_at=row.enrolled_at,
            progress=row.progress,
            completed=row.completed,
            completed_at=row.completed_at,
            updated_at=row.updated_at,
        )
        return enrollment

    async def create(self, enrollment: EnrollmentEntity) -> EnrollmentEntity:
        row = Enrollment(
            user_id=enrollment.user_id,
            course_id=enrollment.course_id,
            enrolled_at=enrollment.enrolled_at,
            progress=enrollment.progress,
            completed=enrollment.completed,
            completed_at=enrollment.completed_at,
            updated_at=enrollment.updated_at,
        )
        self._session.add(row)
        await self._session.flush()
        return self._to_entity(row)

    async def get_by_id(self, enrollment_id: int) -> EnrollmentEntity | None:
        row = await self._session.get(Enrollment, enrollment_id)
        if not row:
            return None
        return self._to_entity(row)

    async def get_by_course_id(self, course_id: int) -> list[EnrollmentEntity]:
        enrollments = await self._session.execute(
            select(Enrollment)
            .where(Enrollment.course_id == course_id)
            .order_by(Enrollment.id)
        )
        rows = enrollments.scalars()
        return [self._to_entity(e) for e in rows]

    async def get_by_user_and_course(
        self, user_id: int, course_id: int
    ) -> EnrollmentEntity | None:
        enrollment = await self._session.execute(
            select(Enrollment).where(
                Enrollment.user_id == user_id, Enrollment.course_id == course_id
            )
        )
        row = enrollment.scalar_one_or_none()
        if not row:
            return None
        return self._to_entity(row)

    async def get_by_user_id(self, user_id: int) -> list[EnrollmentEntity]:
        enrollments = await self._session.execute(
            select(Enrollment)
            .where(Enrollment.user_id == user_id)
            .order_by(Enrollment.id)
        )
        rows = enrollments.scalars()
        return [self._to_entity(e) for e in rows]

    async def update(self, enrollment: EnrollmentEntity) -> EnrollmentEntity:
        enr = await self._session.get(Enrollment, enrollment.id)
        if not enr:
            raise CantBeUpdatedError("Нельзя изменить несуществующую запись")
        enr.completed_at = enrollment.completed_at
        enr.progress = enrollment.progress
        enr.completed = enrollment.completed
        enr.updated_at = enrollment.updated_at = datetime.now(tz=timezone.utc)
        await self._session.flush()
        return self._to_entity(enr)

    async def delete(self, enrollment_id: int) -> None:
        enr = await self._session.get(Enrollment, enrollment_id)
        if not enr:
            return
        await self._session.delete(enr)
        await self._session.flush()
