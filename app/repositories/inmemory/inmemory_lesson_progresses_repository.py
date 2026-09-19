from app.entities.lesson_progress_entity import LessonProgressEntity
from app.exceptions.exceptions import CantBeUpdatedError


class InMemoryLessonProgressRepository:
    def __init__(self):
        self._lesson_progresses: dict[int, LessonProgressEntity] = {}
        self._next_id = 0

    async def create(
        self, lesson_progress: LessonProgressEntity
    ) -> LessonProgressEntity:
        lesson_progress.id = self._next_id
        self._next_id += 1
        self._lesson_progresses[lesson_progress.id] = lesson_progress
        return lesson_progress

    async def get_by_id(self, lesson_progress_id: int) -> LessonProgressEntity | None:
        return self._lesson_progresses.get(lesson_progress_id)

    async def get_by_enrollment_id(
        self, enrollment_id: int
    ) -> list[LessonProgressEntity]:
        lesson_progresses = []
        for lesson_progress in self._lesson_progresses.values():
            if lesson_progress.enrollment_id == enrollment_id:
                lesson_progresses.append(lesson_progress)
        return lesson_progresses

    async def get_by_enrollment_and_lesson(
        self, enrollment_id: int, lesson_id: int
    ) -> LessonProgressEntity | None:
        for lesson_progress in self._lesson_progresses.values():
            if (
                lesson_progress.enrollment_id == enrollment_id
                and lesson_progress.lesson_id == lesson_id
            ):
                return lesson_progress
        return None

    async def update(
        self, lesson_progress: LessonProgressEntity
    ) -> LessonProgressEntity:
        searched_lesson_progress = self._lesson_progresses.get(lesson_progress.id)
        if not searched_lesson_progress:
            raise CantBeUpdatedError("Такого прогресса не существует")
        self._lesson_progresses[lesson_progress.id] = lesson_progress
        return lesson_progress
