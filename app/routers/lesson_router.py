from fastapi import APIRouter, Depends, Query

from app.dependencies.auth_dependencies import get_current_user_id, require_role
from app.dependencies.use_cases_dependencies import (
    get_course_lessons_uc,
    get_create_lesson_uc,
    get_delete_lesson_uc,
    get_lesson_details_uc,
    get_update_lesson_uc,
)
from app.entities.user_entity import UserRole
from app.models.lesson_model import (
    LessonCreate,
    LessonListItem,
    LessonResponse,
    UpdatedLesson,
)
from app.use_cases.create_lesson import LessonCreateUseCase
from app.use_cases.delete_lesson import DeleteLessonUseCase
from app.use_cases.get_course_lessons_list import GetCourseLessonsList
from app.use_cases.get_lesson_details import GetLessonDetailsUseCase
from app.use_cases.update_lesson import UpdateLessonUseCase

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


@lesson_router.get("/courses/{course_id}/lessons", response_model=list[LessonListItem])
async def get_course_lessons(
    course_id: int,
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    get_course_lessons_uc: GetCourseLessonsList = Depends(get_course_lessons_uc),
    user_id: int = Depends(get_current_user_id),
):
    lessons = await get_course_lessons_uc.execute(course_id, user_id)
    return [LessonListItem.model_validate(l) for l in lessons][offset : offset + limit]


@lesson_router.get(
    "/courses/{course_id}/lessons/{lesson_id}", response_model=LessonResponse
)
async def get_lesson_details(
    course_id: int,
    lesson_id: int,
    get_lesson_details_uc: GetLessonDetailsUseCase = Depends(get_lesson_details_uc),
    teacher_id: int = Depends(get_current_user_id),
):
    return LessonResponse.model_validate(
        await get_lesson_details_uc.execute(course_id, lesson_id, teacher_id)
    )


@lesson_router.delete("/courses/{course_id}/lessons/{lesson_id}", status_code=204)
async def delete_lesson(
    course_id: int,
    lesson_id: int,
    teacher_id: int = Depends(get_current_user_id),
    delete_lesson_uc: DeleteLessonUseCase = Depends(get_delete_lesson_uc),
):
    await delete_lesson_uc.execute(course_id, lesson_id, teacher_id)


@lesson_router.patch(
    "/courses/{course_id}/lessons/{lesson_id}", response_model=LessonResponse
)
async def update_lesson(
    course_id: int,
    lesson_id: int,
    lesson_update: UpdatedLesson,
    teacher_id: int = Depends(get_current_user_id),
    update_lesson_uc: UpdateLessonUseCase = Depends(get_update_lesson_uc),
):
    updated_lesson = await update_lesson_uc.execute(
        lesson_id, course_id, teacher_id, lesson_update
    )
    return LessonResponse.model_validate(updated_lesson)
