from fastapi import APIRouter, Depends

from app.dependencies.auth_dependencies import get_current_user_id
from app.dependencies.use_cases_dependencies import get_make_progress_uc
from app.models.lesson_progress_model import LessonProgressResponse
from app.use_cases.make_progress import MakeProgressUseCase

progress_router = APIRouter()


@progress_router.post(
    "/courses/{course_id}/lessons/{lesson_id}/lesson_progress",
    response_model=LessonProgressResponse,
)
async def create_lesson_progress(
    course_id: int,
    lesson_id: int,
    user_id: int = Depends(get_current_user_id),
    make_progress_uc: MakeProgressUseCase = Depends(get_make_progress_uc),
):
    progress = await make_progress_uc.execute(
        course_id=course_id, lesson_id=lesson_id, user_id=user_id
    )
    return LessonProgressResponse.model_validate(progress)
