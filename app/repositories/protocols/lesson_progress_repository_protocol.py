from typing import Protocol

from app.entities.lesson_progress_entity import LessonProgressEntity


class LessonProgressRepository(Protocol):
    async def create(
        self, lesson_progress: LessonProgressEntity
    ) -> LessonProgressEntity: ...
    async def get_by_id(
        self, lesson_progress_id: int
    ) -> LessonProgressEntity | None: ...
    async def get_by_enrollment_id(
        self, enrollment_id: int
    ) -> list[LessonProgressEntity]: ...
    async def get_by_enrollment_and_lesson(
        self, enrollment_id: int, lesson_id: int
    ) -> LessonProgressEntity | None: ...
    async def update(
        self, lesson_progress: LessonProgressEntity
    ) -> LessonProgressEntity: ...
