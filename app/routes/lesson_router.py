from fastapi import APIRouter, Depends

from app.dependencies import (
    get_course_lessons_uc,
    get_create_lesson_uc,
    get_current_user_id,
    get_lesson_details_uc,
    require_role,
)
from app.entities.user_entity import UserRole
from app.models.lesson_model import LessonCreate, LessonListItem, LessonResponse
from app.use_cases.create_lesson import LessonCreateUseCase
from app.use_cases.get_course_lessons_list import GetCourseLessonsList
from app.use_cases.get_lesson_details import GetLessonDetailsUseCase

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
    get_course_lessons_uc: GetCourseLessonsList = Depends(get_course_lessons_uc),
    user_id: int = Depends(get_current_user_id),
):
    lessons = await get_course_lessons_uc.execute(course_id)
    return [LessonListItem.model_validate(l) for l in lessons]


@lesson_router.get(
    "/courses/{course_id}/lessons/{lesson_id}", response_model=LessonResponse
)
async def get_lesson_details(
    course_id: int,
    lesson_id: int,
    get_lesson_details_uc: GetLessonDetailsUseCase = Depends(get_lesson_details_uc),
    teacher_id: int = Depends(require_role(UserRole.TEACHER)),
):
    return await get_lesson_details_uc.execute(course_id, lesson_id)
