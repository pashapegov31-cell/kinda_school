from app.entities.lesson_entity import LessonEntity
from app.exceptions.exceptions import CantBeUpdatedError


class InMemoryLessonRepository:
    def __init__(self):
        self._lessons: dict[int, LessonEntity] = {}
        self._next_id = 0

    async def create(self, lesson: LessonEntity) -> LessonEntity:
        lesson.id = self._next_id
        self._next_id += 1
        self._lessons[lesson.id] = lesson
        return lesson

    async def get_by_course_id(self, course_id: int) -> list[LessonEntity]:
        lessons = []
        for lesson in self._lessons.values():
            if lesson.course_id == course_id:
                lessons.append(lesson)
        return sorted(lessons, key=lambda lesson: lesson.order)

    async def get_by_id(self, lesson_id: int) -> LessonEntity | None:
        return self._lessons.get(lesson_id)

    async def update(self, lesson: LessonEntity) -> LessonEntity:
        searched_lesson = self._lessons.get(lesson.id)
        if not searched_lesson:
            raise CantBeUpdatedError("Такого урока не существует")
        self._lessons[lesson.id] = lesson
        return lesson

    async def delete(self, lesson_id: int) -> None:
        searched_lesson = self._lessons.get(lesson_id)
        if searched_lesson:
            del self._lessons[lesson_id]
