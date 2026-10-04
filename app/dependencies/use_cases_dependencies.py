from fastapi import Depends

from app.dependencies.auth_dependencies import token_service
from app.dependencies.switch_repos import (
    get_courses_repo,
    get_enrollments_repo,
    get_lessons_progress_repo,
    get_lessons_repo,
    get_users_repo,
)
from app.use_cases.change_user_role import ChangeUserRoleUseCase
from app.use_cases.create_course import CreateCourseUseCase
from app.use_cases.create_lesson import LessonCreateUseCase
from app.use_cases.delete_course import DeleteCourseUseCase
from app.use_cases.delete_enrollment import DeleteEnrollmentUseCase
from app.use_cases.delete_lesson import DeleteLessonUseCase
from app.use_cases.enroll_in_course import EnrollInCourseUseCase
from app.use_cases.get_course_lessons_list import GetCourseLessonsList
from app.use_cases.get_lesson_details import GetLessonDetailsUseCase
from app.use_cases.login_user import LoginUserUseCase
from app.use_cases.make_progress import MakeProgressUseCase
from app.use_cases.publish_course import PublishCourseUseCase
from app.use_cases.registrate_user import RegisterUserUseCase
from app.use_cases.update_lesson import UpdateLessonUseCase


def get_register_uc(
    users_repo=Depends(get_users_repo),
):
    return RegisterUserUseCase(users_repo, token_service)


def get_login_uc(
    users_repo=Depends(get_users_repo),
):
    return LoginUserUseCase(users_repo, token_service)


def get_create_course_uc(
    courses_repo=Depends(get_courses_repo),
    lessons_repo=Depends(get_lessons_repo),
):
    return CreateCourseUseCase(courses_repo, lessons_repo)


def get_change_user_role_uc(
    users_repo=Depends(get_users_repo),
):
    return ChangeUserRoleUseCase(users_repo)


def get_publish_course_uc(
    courses_repo=Depends(get_courses_repo),
):
    return PublishCourseUseCase(courses_repo)


def get_create_lesson_uc(
    lessons_repo=Depends(get_lessons_repo),
    courses_repo=Depends(get_courses_repo),
):
    return LessonCreateUseCase(lessons_repo, courses_repo)


def get_course_lessons_uc(
    lessons_repo=Depends(get_lessons_repo),
    courses_repo=Depends(get_courses_repo),
):
    return GetCourseLessonsList(courses_repo, lessons_repo)


def get_lesson_details_uc(
    lessons_repo=Depends(get_lessons_repo),
    courses_repo=Depends(get_courses_repo),
    enrollments_repo=Depends(get_enrollments_repo),
):
    return GetLessonDetailsUseCase(lessons_repo, courses_repo, enrollments_repo)


def get_enroll_in_course_uc(
    users_repo=Depends(get_users_repo),
    courses_repo=Depends(get_courses_repo),
    enrollments_repo=Depends(get_enrollments_repo),
):
    return EnrollInCourseUseCase(enrollments_repo, courses_repo, users_repo)


def get_delete_course_uc(
    users_repo=Depends(get_users_repo),
    lessons_repo=Depends(get_lessons_repo),
    courses_repo=Depends(get_courses_repo),
    lesson_progresses_repo=Depends(get_lessons_progress_repo),
    enrollments_repo=Depends(get_enrollments_repo),
):
    return DeleteCourseUseCase(
        courses_repo, users_repo, lessons_repo, lesson_progresses_repo, enrollments_repo
    )


def get_delete_lesson_uc(
    users_repo=Depends(get_users_repo),
    lessons_repo=Depends(get_lessons_repo),
    courses_repo=Depends(get_courses_repo),
    lesson_progresses_repo=Depends(get_lessons_progress_repo),
    get_delete_course_uc=Depends(get_delete_course_uc),
):
    return DeleteLessonUseCase(
        lessons_repo,
        courses_repo,
        users_repo,
        lesson_progresses_repo,
        get_delete_course_uc,
    )


def get_update_lesson_uc(
    users_repo=Depends(get_users_repo),
    lessons_repo=Depends(get_lessons_repo),
    courses_repo=Depends(get_courses_repo),
):
    return UpdateLessonUseCase(lessons_repo, courses_repo, users_repo)


def get_delete_enrollment_uc(
    lesson_progresses_repo=Depends(get_lessons_progress_repo),
    enrollments_repo=Depends(get_enrollments_repo),
):
    return DeleteEnrollmentUseCase(enrollments_repo, lesson_progresses_repo)


def get_make_progress_uc(
    lessons_repo=Depends(get_lessons_repo),
    courses_repo=Depends(get_courses_repo),
    lesson_progresses_repo=Depends(get_lessons_progress_repo),
    enrollments_repo=Depends(get_enrollments_repo),
):
    return MakeProgressUseCase(
        lesson_progresses_repo, enrollments_repo, lessons_repo, courses_repo
    )
