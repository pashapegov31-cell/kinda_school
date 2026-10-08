from fastapi import APIRouter, Depends

from app.dependencies.auth_dependencies import get_current_user_id
from app.dependencies.switch_repos import get_enrollments_repo
from app.dependencies.use_cases_dependencies import (
    get_delete_enrollment_uc,
    get_enroll_in_course_uc,
)
from app.models.enrollment_model import EnrollmentResponse
from app.repositories.protocols.enrollment_repository_protocol import (
    EnrollmentRepository,
)
from app.use_cases.delete_enrollment import DeleteEnrollmentUseCase
from app.use_cases.enroll_in_course import EnrollInCourseUseCase

enrollment_router = APIRouter()


@enrollment_router.post(
    "/courses/{course_id}/enroll", response_model=EnrollmentResponse
)
async def enroll_in_course(
    course_id: int,
    student_id: int = Depends(get_current_user_id),
    enroll_in_course_uc: EnrollInCourseUseCase = Depends(get_enroll_in_course_uc),
):
    enrollment = await enroll_in_course_uc.execute(student_id, course_id)
    return EnrollmentResponse.model_validate(enrollment)


@enrollment_router.delete("/courses/{course_id}/enroll", status_code=204)
async def delete_enrollment(
    course_id: int,
    user_id: int = Depends(get_current_user_id),
    delete_enrollment_uc: DeleteEnrollmentUseCase = Depends(get_delete_enrollment_uc),
):
    await delete_enrollment_uc.execute(user_id, course_id)


@enrollment_router.get("/enrollments/me", response_model=list[EnrollmentResponse])
async def my_enrollments(
    user_id: int = Depends(get_current_user_id),
    enrollments_repo: EnrollmentRepository = Depends(get_enrollments_repo),
):
    enrollments = await enrollments_repo.get_by_user_id(user_id)
    return [EnrollmentResponse.model_validate(e) for e in enrollments]
