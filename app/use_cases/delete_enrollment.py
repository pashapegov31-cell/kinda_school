from app.exceptions.exceptions import NotFoundError
from app.repositories.protocols.enrollment_repository_protocol import (
    EnrollmentRepository,
)
from app.repositories.protocols.lesson_progress_repository_protocol import (
    LessonProgressRepository,
)


class DeleteEnrollmentUseCase:
    def __init__(
        self,
        enrollments_repo: EnrollmentRepository,
        lesson_progress_repo: LessonProgressRepository,
    ):
        self._enrollments_repo = enrollments_repo
        self._lesson_progress_repo = lesson_progress_repo

    async def execute(self, user_id: int, course_id: int):
        enrollment = await self._enrollments_repo.get_by_user_and_course(
            user_id, course_id
        )
        if not enrollment:
            raise NotFoundError("Запись не найдена")
        progresses = await self._lesson_progress_repo.get_by_enrollment_id(
            enrollment.id
        )
        for progress in progresses:
            await self._lesson_progress_repo.delete(progress.id)
        await self._enrollments_repo.delete(enrollment.id)
