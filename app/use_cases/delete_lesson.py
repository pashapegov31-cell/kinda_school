from app.entities.user_entity import UserRole
from app.exceptions.exceptions import ForbiddenError, NotFoundError
from app.repositories.protocols.course_repository_protocol import CourseRepository
from app.repositories.protocols.lesson_progress_repository_protocol import (
    LessonProgressRepository,
)
from app.repositories.protocols.lesson_repository_protocol import LessonRepository
from app.repositories.protocols.users_repository_protocol import UsersRepository
from app.use_cases.delete_course import DeleteCourseUseCase


class DeleteLessonUseCase:
    def __init__(
        self,
        lesson_repo: LessonRepository,
        course_repo: CourseRepository,
        users_repo: UsersRepository,
        lessons_progress_repo: LessonProgressRepository,
        delete_course_uc: DeleteCourseUseCase,
    ):
        self._lesson_repo = lesson_repo
        self._course_repo = course_repo
        self._users_repo = users_repo
        self._lessons_progress_repo = lessons_progress_repo
        self._delete_course_uc = delete_course_uc

    async def execute(self, course_id: int, lesson_id: int, teacher_id: int):
        course = await self._course_repo.get_by_id(course_id)
        if not course:
            raise NotFoundError("Курс не найден")
        teacher = await self._users_repo.get_by_id(teacher_id)
        if not teacher:
            raise NotFoundError("Пользователя с таким айди не существует")

        if course.teacher_id != teacher_id and teacher.role != UserRole.ADMIN:
            raise ForbiddenError("Вы не можете удалять уроки не из своего курса")

        lesson = await self._lesson_repo.get_by_id(lesson_id)
        if not lesson:
            raise NotFoundError("Урок не найден")
        if lesson.course_id != course_id:
            raise NotFoundError("Урок не найден в этом курсе")
        lessons = await self._lesson_repo.get_by_course_id(course_id)
        if len(lessons) == 1:
            await self._delete_course_uc.execute(course_id, teacher_id)
        else:
            lesson_progresses = await self._lessons_progress_repo.get_by_lesson_id(
                lesson_id
            )
            for progress in lesson_progresses:
                await self._lessons_progress_repo.delete(progress.id)
            for l in lessons[lesson.order :]:
                l.order -= 1
                await self._lesson_repo.update(l)
            await self._lesson_repo.delete(lesson_id)
