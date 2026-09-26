from fastapi import APIRouter, Depends

from app.dependencies import (
    get_create_lesson_uc,
    require_role,
)
from app.entities.user_entity import UserRole
from app.models.lesson_model import LessonCreate, LessonResponse
from app.use_cases.create_lesson import LessonCreateUseCase

lesson_router = APIRouter()


@lesson_router.post("/courses/{course_id}/lessons", response_model=LessonResponse)
async def create_lesson(
    lesson: LessonCreate,
    course_id: int,
    teacher_id: int = Depends(require_role(UserRole.TEACHER)),
    create_lesson_uc: LessonCreateUseCase = Depends(get_create_lesson_uc),
):
    created_lesson = await create_lesson_uc.execute(
        lesson=lesson,
        after_lesson_id=lesson.after_lesson_id,
        course_id=course_id,
        teacher_id=teacher_id,
    )
    return LessonResponse.model_validate(created_lesson)
