from fastapi import APIRouter, Depends

from app.dependencies import (
    get_create_course_uc,
    require_role,
)
from app.entities.user_entity import UserRole
from app.models.course_model import CourseCreate, CourseResponse
from app.use_cases.create_course import CreateCourseUseCase

course_router = APIRouter()


@course_router.post("/courses", response_model=CourseResponse)
async def course_create(
    new_course: CourseCreate,
    create_course_uc: CreateCourseUseCase = Depends(get_create_course_uc),
    teacher_id: int = Depends(require_role(role=UserRole.TEACHER)),
):
    course = await create_course_uc.execute(new_course, teacher_id)
    return CourseResponse(
        id=course.id,
        teacher_id=teacher_id,
        title=course.title,
        description=course.description,
        price=course.price,
        status=course.status,
        created_at=course.created_at,
    )
