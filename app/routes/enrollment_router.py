from fastapi import APIRouter, Depends

from app.dependencies import get_current_user_id, get_enroll_in_course_uc
from app.models.enrollment_model import EnrollmentResponse
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
