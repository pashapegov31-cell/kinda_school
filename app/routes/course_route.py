from fastapi import APIRouter, Depends, HTTPException, Query

from app.dependencies import (
    get_course_lessons_uc,
    get_create_course_uc,
    get_current_user_id,
    get_inmemory_courses_repo,
    get_publish_course_uc,
    require_role,
)
from app.entities.user_entity import UserRole
from app.exceptions.exceptions import CantBeUpdatedError, ForbiddenError
from app.models.course_model import CourseCreate, CourseResponse
from app.models.lesson_model import LessonListItem
from app.repositories.protocols.course_repository_protocol import CourseRepository
from app.use_cases.create_course import CreateCourseUseCase
from app.use_cases.get_course_lessons_list import GetCourseLessonsList
from app.use_cases.publish_course import PublishCourseUseCase

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


@course_router.get("/courses", response_model=list[CourseResponse])
async def get_courses(
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    courses_repo: CourseRepository = Depends(get_inmemory_courses_repo),
):
    courses = await courses_repo.get_published()
    return [
        CourseResponse.model_validate(course)
        for course in courses[offset : offset + limit]
    ]


@course_router.get("/courses/mine", response_model=list[CourseResponse])
async def get_own_courses(
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    teacher_id: int = Depends(require_role(UserRole.TEACHER)),
    courses_repo: CourseRepository = Depends(get_inmemory_courses_repo),
):
    own_courses = await courses_repo.get_by_teacher_id(teacher_id)
    return [
        CourseResponse.model_validate(course)
        for course in own_courses[offset : offset + limit]
    ]


@course_router.post("/courses/{course_id}/publish", response_model=CourseResponse)
async def publish(
    course_id: int,
    teacher_id: int = Depends(require_role(UserRole.TEACHER)),
    publish_course_uc: PublishCourseUseCase = Depends(get_publish_course_uc),
):
    try:
        return CourseResponse.model_validate(
            await publish_course_uc.execute(course_id, teacher_id)
        )
    except CantBeUpdatedError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ForbiddenError as e:
        raise HTTPException(status_code=403, detail=str(e))


@course_router.get("/courses/{course_id}/lessons", response_model=list[LessonListItem])
async def get_course_lessons(
    course_id: int,
    get_course_lessons_uc: GetCourseLessonsList = Depends(get_course_lessons_uc),
    user_id: int = Depends(get_current_user_id),
):
    lessons = await get_course_lessons_uc.execute(course_id)
    return [LessonListItem.model_validate(l) for l in lessons]
