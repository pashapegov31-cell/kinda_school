from datetime import datetime, timezone

from app.entities.lesson_progress_entity import LessonProgressEntity
from app.exceptions.exceptions import NotFoundError
from app.repositories.protocols.course_repository_protocol import CourseRepository
from app.repositories.protocols.enrollment_repository_protocol import (
    EnrollmentRepository,
)
from app.repositories.protocols.lesson_progress_repository_protocol import (
    LessonProgressRepository,
)
from app.repositories.protocols.lesson_repository_protocol import LessonRepository


class MakeProgressUseCase:
    def __init__(
        self,
        lessons_progress_repo: LessonProgressRepository,
        enrollments_repo: EnrollmentRepository,
        lessons_repo: LessonRepository,
        courses_repo: CourseRepository,
    ):
        self._lessons_progress_repo = lessons_progress_repo
        self._enrollments_repo = enrollments_repo
        self._lessons_repo = lessons_repo
        self._courses_repo = courses_repo

    async def execute(
        self, user_id: int, course_id: int, lesson_id: int
    ) -> LessonProgressEntity:
        enrollment = await self._enrollments_repo.get_by_user_and_course(
            user_id, course_id
        )
        course = await self._courses_repo.get_by_id(course_id)
        if not course:
            raise NotFoundError("Курс не найден")
        lesson = await self._lessons_repo.get_by_id(lesson_id)
        if not lesson:
            raise NotFoundError("Урок не найден")
        if lesson.course_id != course_id:
            raise NotFoundError("Урок в этом курсе не найден")
        if not enrollment:
            raise NotFoundError("Вы не записаны на этот курс")
        lesson_progress = (
            await self._lessons_progress_repo.get_by_enrollment_and_lesson(
                enrollment.id, lesson_id
            )
        )
        if not lesson_progress:
            lesson_progress = await self._lessons_progress_repo.create(
                LessonProgressEntity(
                    id=0,
                    enrollment_id=enrollment.id,
                    lesson_id=lesson_id,
                    completed=True,
                    completed_at=datetime.now(timezone.utc),
                )
            )
        else:
            return lesson_progress

        lesson_progresses = await self._lessons_progress_repo.get_by_enrollment_id(
            enrollment.id
        )
        completed_lessons = 0
        for progress in lesson_progresses:
            if progress.completed:
                completed_lessons += 1
        lessons = await self._lessons_repo.get_by_course_id(course_id)
        enrollment.progress = int(completed_lessons / len(lessons) * 100)
        if enrollment.progress == len(lessons) and not enrollment.completed:
            enrollment.completed = True
            enrollment.completed_at = datetime.now(timezone.utc)
        await self._enrollments_repo.update(enrollment)
        return lesson_progress
