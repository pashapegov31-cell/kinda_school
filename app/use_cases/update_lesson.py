from app.entities.lesson_entity import LessonEntity
from app.entities.user_entity import UserRole
from app.exceptions.exceptions import ForbiddenError, NotFoundError
from app.models.lesson_model import UpdatedLesson
from app.repositories.protocols.course_repository_protocol import CourseRepository
from app.repositories.protocols.lesson_repository_protocol import LessonRepository
from app.repositories.protocols.users_repository_protocol import UsersRepository


class UpdateLessonUseCase:
    def __init__(
        self,
        lessons_repo: LessonRepository,
        courses_repo: CourseRepository,
        users_repo: UsersRepository,
    ):
        self._lessons_repo = lessons_repo
        self._courses_repo = courses_repo
        self._users_repo = users_repo

    async def execute(
        self,
        lesson_id: int,
        course_id: int,
        teacher_id: int,
        updated_lesson: UpdatedLesson,
    ) -> LessonEntity:
        teacher = await self._users_repo.get_by_id(teacher_id)
        if not teacher:
            raise NotFoundError("Пользователь с таким айди не найден")
        course = await self._courses_repo.get_by_id(course_id)
        if not course:
            raise NotFoundError("Курс не найден")
        if course.teacher_id != teacher_id and teacher.role != UserRole.ADMIN:
            raise ForbiddenError("Вы не можете изменять чужой урок")
        lesson = await self._lessons_repo.get_by_id(lesson_id)
        if not lesson:
            raise NotFoundError("Урок не найден")
        if lesson.course_id != course_id:
            raise NotFoundError("Такого урока нет в этом курсе")
        title = updated_lesson.title
        if title is not None:
            lesson.title = title
        content = updated_lesson.content
        if content is not None:
            lesson.content = content
        video_url = updated_lesson.video_url
        if video_url is not None:
            lesson.video_url = video_url
        duration_minutes = updated_lesson.duration_minutes
        if duration_minutes is not None:
            lesson.duration_minutes = duration_minutes
        return await self._lessons_repo.update(lesson)
