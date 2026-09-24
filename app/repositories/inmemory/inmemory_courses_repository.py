from app.entities.course_entity import CourseEntity, CourseStatus
from app.exceptions.exceptions import CantBeUpdatedError


class InMemoryCourseRepository:
    def __init__(self):
        self._courses: dict[int, CourseEntity] = {}
        self._next_id = 0

    async def create(self, course: CourseEntity) -> CourseEntity:
        course.id = self._next_id
        self._next_id += 1
        self._courses[course.id] = course
        return course

    async def get_by_id(self, course_id: int) -> CourseEntity | None:
        return self._courses.get(course_id)

    async def get_by_teacher_id(self, teacher_id: int) -> list[CourseEntity]:
        courses = []
        for course in self._courses.values():
            if course.teacher_id == teacher_id:
                courses.append(course)
        return courses

    async def get_published(self) -> list[CourseEntity]:
        courses = []
        for course in self._courses.values():
            if course.status == CourseStatus.PUBLISHED:
                courses.append(course)
        return courses

    async def update(self, course: CourseEntity) -> CourseEntity:
        searched_course = self._courses.get(course.id)
        if not searched_course:
            raise CantBeUpdatedError("Такого курса не существует")
        self._courses[course.id] = course
        return course

    async def delete(self, course_id: int) -> None:
        searched_course = self._courses.get(course_id)
        if searched_course:
            del self._courses[course_id]

    async def get_all_courses(self) -> list[CourseEntity]:
        return list(self._courses.values())
