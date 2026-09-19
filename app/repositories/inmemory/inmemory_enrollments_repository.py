from app.entities.enrollment_entity import EnrollmentEntity
from app.exceptions.exceptions import CantBeUpdatedError


class InMemoryEnrollmentRepository:
    def __init__(self):
        self._enrollments: dict[int, EnrollmentEntity] = {}
        self._next_id = 0

    async def create(self, enrollment: EnrollmentEntity) -> EnrollmentEntity:
        enrollment.id = self._next_id
        self._next_id += 1
        self._enrollments[enrollment.id] = enrollment
        return enrollment

    async def update(self, enrollment: EnrollmentEntity) -> EnrollmentEntity:
        searched_enrollment = self._enrollments.get(enrollment.id)
        if not searched_enrollment:
            raise CantBeUpdatedError("Такой записи не существует")
        self._enrollments[enrollment.id] = enrollment
        return searched_enrollment

    async def get_by_id(self, enrollment_id: int) -> EnrollmentEntity | None:
        return self._enrollments.get(enrollment_id)

    async def get_by_user_id(self, user_id: int) -> list[EnrollmentEntity]:
        enrollments = []
        for enrollment in self._enrollments.values():
            if enrollment.user_id == user_id:
                enrollments.append(enrollment)
        return enrollments

    async def get_by_user_and_course(
        self, user_id: int, course_id: int
    ) -> EnrollmentEntity | None:
        for enrollment in self._enrollments.values():
            if enrollment.user_id == user_id and enrollment.course_id == course_id:
                return enrollment
        return None

    async def get_by_course_id(self, course_id: int) -> list[EnrollmentEntity]:
        enrollments = []
        for enrollment in self._enrollments.values():
            if enrollment.course_id == course_id:
                enrollments.append(enrollment)
        return enrollments
