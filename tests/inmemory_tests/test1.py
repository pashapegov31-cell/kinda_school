"""
Синхронные тесты MVP-ядра kinda_school.
Нужно: pip install pytest httpx   (pytest-asyncio НЕ нужен)
Конфиг (pytest.ini в корне):
    [pytest]
    pythonpath = .
    testpaths = tests
"""

import asyncio

import pytest
from fastapi.testclient import TestClient

import app.dependencies as deps
import app.seed_admin as seed_mod
from app.core.config_settings import settings
from app.exceptions.exceptions import NotValidPrice
from app.repositories.inmemory.inmemory_courses_repository import (
    InMemoryCourseRepository,
)
from app.repositories.inmemory.inmemory_enrollments_repository import (
    InMemoryEnrollmentRepository,
)
from app.repositories.inmemory.inmemory_lesson_progresses_repository import (
    InMemoryLessonProgressRepository,
)
from app.repositories.inmemory.inmemory_lessons_repository import (
    InMemoryLessonRepository,
)
from app.repositories.inmemory.inmemory_users_repository import InMemoryUsersRepository
from main import app

P = "/v1"
PASSWORD = "Str0ng!pass1"
BASE_LESSON_TITLE = "Это мой первый урок в данном курсе"


def probe(coro):
    """Синхронный зонд в inmemory-репозиторий."""
    return asyncio.run(coro)


def hdr(token):
    return {"Authorization": f"Bearer {token}"}


# ------------------------------- фикстуры -------------------------------
@pytest.fixture()
def client():
    deps.users_repo = InMemoryUsersRepository()
    deps.courses_repo = InMemoryCourseRepository()
    deps.lessons_repo = InMemoryLessonRepository()
    deps.enrollments_repo = InMemoryEnrollmentRepository()
    deps.lessons_progress_repo = InMemoryLessonProgressRepository()
    seed_mod.users_repo = deps.users_repo
    with TestClient(app) as c:  # lifespan сеет админа в СВЕЖИЕ репозитории
        yield c


def test_me_without_token_401(client):
    # В вашей сборке отсутствие заголовка даёт 401 (а не дефолтные 403 от HTTPBearer)
    assert client.get(f"{P}/me").status_code == 401


def login(client, email, password=PASSWORD):
    r = client.post(f"{P}/login", json={"email": email, "password": password})
    assert r.status_code == 200, r.text
    return r.json()["access_token"]


@pytest.fixture()
def admin_token(client):
    return login(client, settings.ADMIN_EMAIL, settings.ADMIN_PASSWORD)


@pytest.fixture()
def student(client):
    email = "student@school.io"
    r = client.post(
        f"{P}/register", json={"email": email, "name": "Student", "password": PASSWORD}
    )
    assert r.status_code == 200, r.text
    return {"token": r.json()["access_token"], "email": email}


def _make_teacher(client, admin_token, email):
    r = client.post(
        f"{P}/register",
        json={"email": email, "name": email.split("@")[0], "password": PASSWORD},
    )
    assert r.status_code == 200, r.text
    uid = probe(deps.users_repo.get_by_email(email)).id  # id в API не возвращается
    r = client.post(
        f"{P}/change/role",
        json={"user_id": uid, "new_role": "teacher"},
        headers=hdr(admin_token),
    )
    assert r.status_code == 200, r.text
    return {"token": login(client, email), "email": email, "id": uid}


@pytest.fixture()
def teacher(client, admin_token):
    return _make_teacher(client, admin_token, "teacher@school.io")


@pytest.fixture()
def teacher2(client, admin_token):
    return _make_teacher(client, admin_token, "teacher2@school.io")


def draft_course(client, token, title="Math"):
    r = client.post(
        f"{P}/courses",
        json={"title": title, "description": "d", "price": 100},
        headers=hdr(token),
    )
    assert r.status_code == 200, r.text
    course = r.json()
    return {
        "course": course,
        "lessons": probe(deps.lessons_repo.get_by_course_id(course["id"])),
    }


def published_course(client, token, title="Pub"):
    dc = draft_course(client, token, title)
    r = client.post(f"{P}/courses/{dc['course']['id']}/publish", headers=hdr(token))
    assert r.status_code == 200, r.text
    return dc


# ================================== AUTH ==================================
def test_register_returns_bearer_token(client):
    r = client.post(
        f"{P}/register", json={"email": "a@b.io", "name": "A", "password": PASSWORD}
    )
    assert r.status_code == 200
    assert r.json()["token_type"] == "Bearer"
    assert probe(deps.users_repo.get_by_email("a@b.io")).role.value == "student"


def test_register_duplicate_email_400(client):
    client.post(
        f"{P}/register", json={"email": "dup@b.io", "name": "A", "password": PASSWORD}
    )
    r = client.post(
        f"{P}/register", json={"email": "dup@b.io", "name": "B", "password": PASSWORD}
    )
    assert r.status_code == 400


def test_login_ok(client, student):
    assert login(client, student["email"])


def test_login_wrong_password_400(client, student):
    r = client.post(f"{P}/login", json={"email": student["email"], "password": "wrong"})
    assert r.status_code == 400  # LoginError мапится в 400 в роуте


def test_login_unknown_email_400(client):
    assert (
        client.post(
            f"{P}/login", json={"email": "ghost@b.io", "password": PASSWORD}
        ).status_code
        == 400
    )


# ================================== /ME ==================================
def test_me_returns_profile(client, student):
    r = client.get(f"{P}/me", headers=hdr(student["token"]))
    assert r.status_code == 200
    assert r.json()["email"] == student["email"] and r.json()["role"] == "student"


def test_me_with_bad_token_401(client):
    assert (
        client.get(f"{P}/me", headers={"Authorization": "Bearer garbage"}).status_code
        == 401
    )


# ============================== CHANGE ROLE ==============================
def test_admin_can_promote(client, admin_token, student):
    uid = probe(deps.users_repo.get_by_email(student["email"])).id
    r = client.post(
        f"{P}/change/role",
        json={"user_id": uid, "new_role": "teacher"},
        headers=hdr(admin_token),
    )
    assert r.status_code == 200 and r.json()["role"] == "teacher"


def test_non_admin_cannot_change_role(client, student):
    r = client.post(
        f"{P}/change/role",
        json={"user_id": 1, "new_role": "teacher"},
        headers=hdr(student["token"]),
    )
    assert r.status_code == 403


# ================================ COURSES ================================
def test_teacher_creates_draft_with_base_lesson(client, teacher):
    dc = draft_course(client, teacher["token"])
    assert dc["course"]["status"] == "draft"
    assert len(dc["lessons"]) == 1 and dc["lessons"][0].order == 1


def test_student_cannot_create_course(client, student):
    r = client.post(
        f"{P}/courses",
        json={"title": "X", "description": "x", "price": 0},
        headers=hdr(student["token"]),
    )
    assert r.status_code == 403


def test_negative_price_raises(client, teacher):
    # NotValidPrice НЕ имеет HTTP-хендлера в main.py — исключение прорывается наружу.
    # Добавите хендлер (400) — замените на assert r.status_code == 400.
    with pytest.raises(NotValidPrice):
        client.post(
            f"{P}/courses",
            json={"title": "X", "description": "x", "price": -1},
            headers=hdr(teacher["token"]),
        )


def test_catalog_only_published(client, teacher):
    draft_course(client, teacher["token"], "DraftCourse")
    published_course(client, teacher["token"], "PubCourse")
    titles = {c["title"] for c in client.get(f"{P}/courses").json()}
    assert "PubCourse" in titles and "DraftCourse" not in titles


def test_mine_returns_all_own_courses(client, teacher):
    draft_course(client, teacher["token"], "D")
    published_course(client, teacher["token"], "P")
    titles = {
        c["title"]
        for c in client.get(f"{P}/courses/mine", headers=hdr(teacher["token"])).json()
    }
    assert titles == {"D", "P"}


def test_publish_by_owner(client, teacher):
    dc = draft_course(client, teacher["token"])
    r = client.post(
        f"{P}/courses/{dc['course']['id']}/publish", headers=hdr(teacher["token"])
    )
    assert r.status_code == 200 and r.json()["status"] == "published"


def test_publish_by_other_teacher_403(client, teacher, teacher2):
    dc = draft_course(client, teacher["token"])
    r = client.post(
        f"{P}/courses/{dc['course']['id']}/publish", headers=hdr(teacher2["token"])
    )
    assert r.status_code == 403


def test_publish_twice_404(client, teacher):
    dc = published_course(client, teacher["token"])
    r = client.post(
        f"{P}/courses/{dc['course']['id']}/publish", headers=hdr(teacher["token"])
    )
    assert r.status_code == 404  # CantBeUpdatedError мапится в 404 в роуте


def test_publish_by_admin_403(client, admin_token, teacher):
    dc = draft_course(client, teacher["token"])
    r = client.post(
        f"{P}/courses/{dc['course']['id']}/publish", headers=hdr(admin_token)
    )
    assert r.status_code == 403  # политика: админ не публикует чужое


# ================================ LESSONS ================================
def test_create_lesson_after_anchor(client, teacher):
    dc = draft_course(client, teacher["token"])
    cid = dc["course"]["id"]
    r = client.post(
        f"{P}/courses/{cid}/lessons",
        json={
            "title": "L2",
            "content": "x",
            "video_url": None,
            "after_lesson_id": dc["lessons"][0].id,
        },
        headers=hdr(teacher["token"]),
    )
    assert r.status_code == 200 and r.json()["order"] == 2


def test_insert_in_middle_shifts_tail(client, teacher):
    dc = draft_course(client, teacher["token"])
    cid = dc["course"]["id"]
    l2 = client.post(
        f"{P}/courses/{cid}/lessons",
        json={
            "title": "L2",
            "content": "x",
            "video_url": None,
            "after_lesson_id": dc["lessons"][0].id,
        },
        headers=hdr(teacher["token"]),
    ).json()
    client.post(
        f"{P}/courses/{cid}/lessons",
        json={
            "title": "L3",
            "content": "x",
            "video_url": None,
            "after_lesson_id": l2["id"],
        },
        headers=hdr(teacher["token"]),
    )
    client.post(
        f"{P}/courses/{cid}/lessons",
        json={
            "title": "L2.5",
            "content": "x",
            "video_url": None,
            "after_lesson_id": l2["id"],
        },
        headers=hdr(teacher["token"]),
    )
    orders = {l.title: l.order for l in probe(deps.lessons_repo.get_by_course_id(cid))}
    assert orders == {BASE_LESSON_TITLE: 1, "L2": 2, "L2.5": 3, "L3": 4}


def test_create_lesson_bad_anchor_404(client, teacher):
    dc = draft_course(client, teacher["token"])
    r = client.post(
        f"{P}/courses/{dc['course']['id']}/lessons",
        json={
            "title": "X",
            "content": "x",
            "video_url": None,
            "after_lesson_id": 999999,
        },
        headers=hdr(teacher["token"]),
    )
    assert r.status_code == 404


def test_create_lesson_in_foreign_course_403(client, student, teacher):
    dc = draft_course(client, teacher["token"])
    r = client.post(
        f"{P}/courses/{dc['course']['id']}/lessons",
        json={
            "title": "X",
            "content": "x",
            "video_url": None,
            "after_lesson_id": dc["lessons"][0].id,
        },
        headers=hdr(student["token"]),
    )
    assert r.status_code == 403


def test_owner_sees_draft_lessons(client, teacher):
    dc = draft_course(client, teacher["token"])
    r = client.get(
        f"{P}/courses/{dc['course']['id']}/lessons", headers=hdr(teacher["token"])
    )
    assert r.status_code == 200 and len(r.json()) == 1


def test_outsider_sees_draft_lessons_404(client, student, teacher):
    dc = draft_course(client, teacher["token"])
    r = client.get(
        f"{P}/courses/{dc['course']['id']}/lessons", headers=hdr(student["token"])
    )
    assert r.status_code == 404


def test_published_lessons_visible_without_content(client, student, teacher):
    pub = published_course(client, teacher["token"])
    items = client.get(
        f"{P}/courses/{pub['course']['id']}/lessons", headers=hdr(student["token"])
    ).json()
    assert items and "content" not in items[0] and "title" in items[0]


def test_details_requires_enrollment(client, student, teacher):
    pub = published_course(client, teacher["token"])
    cid, lid = pub["course"]["id"], pub["lessons"][0].id
    assert (
        client.get(
            f"{P}/courses/{cid}/lessons/{lid}", headers=hdr(student["token"])
        ).status_code
        == 403
    )
    client.post(f"{P}/courses/{cid}/enroll", headers=hdr(student["token"]))
    r = client.get(f"{P}/courses/{cid}/lessons/{lid}", headers=hdr(student["token"]))
    assert r.status_code == 200 and "content" in r.json()


def test_update_partial_keeps_other_fields(client, teacher):
    dc = draft_course(client, teacher["token"])
    cid, lid = dc["course"]["id"], dc["lessons"][0].id
    r = client.patch(
        f"{P}/courses/{cid}/lessons/{lid}",
        json={"title": "Renamed"},
        headers=hdr(teacher["token"]),
    )
    assert r.status_code == 200
    body = r.json()
    assert (
        body["title"] == "Renamed"
        and body["content"] == "Здесь будет контент"
        and body["order"] == 1
    )


def test_update_foreign_by_admin_200(client, admin_token, teacher):
    dc = draft_course(client, teacher["token"])
    r = client.patch(
        f"{P}/courses/{dc['course']['id']}/lessons/{dc['lessons'][0].id}",
        json={"title": "Moderated"},
        headers=hdr(admin_token),
    )
    assert r.status_code == 200 and r.json()["title"] == "Moderated"


def test_update_foreign_by_other_teacher_403(client, teacher, teacher2):
    dc = draft_course(client, teacher["token"])
    r = client.patch(
        f"{P}/courses/{dc['course']['id']}/lessons/{dc['lessons'][0].id}",
        json={"title": "Hack"},
        headers=hdr(teacher2["token"]),
    )
    assert r.status_code == 403


def test_delete_last_lesson_cascades_course(client, teacher):
    dc = draft_course(client, teacher["token"])
    cid, lid = dc["course"]["id"], dc["lessons"][0].id
    assert (
        client.delete(
            f"{P}/courses/{cid}/lessons/{lid}", headers=hdr(teacher["token"])
        ).status_code
        == 204
    )
    assert probe(deps.courses_repo.get_by_id(cid)) is None
    assert probe(deps.lessons_repo.get_by_id(lid)) is None


def test_delete_middle_renumbers(client, teacher):
    dc = draft_course(client, teacher["token"])
    cid = dc["course"]["id"]
    l2 = client.post(
        f"{P}/courses/{cid}/lessons",
        json={
            "title": "L2",
            "content": "x",
            "video_url": None,
            "after_lesson_id": dc["lessons"][0].id,
        },
        headers=hdr(teacher["token"]),
    ).json()
    client.delete(
        f"{P}/courses/{cid}/lessons/{l2['id']}", headers=hdr(teacher["token"])
    )
    orders = {l.title: l.order for l in probe(deps.lessons_repo.get_by_course_id(cid))}
    assert orders == {BASE_LESSON_TITLE: 1}


def test_delete_foreign_lesson_403(client, teacher, teacher2):
    dc = draft_course(client, teacher["token"])
    r = client.delete(
        f"{P}/courses/{dc['course']['id']}/lessons/{dc['lessons'][0].id}",
        headers=hdr(teacher2["token"]),
    )
    assert r.status_code == 403


def test_delete_by_admin_204(client, admin_token, teacher):
    dc = draft_course(client, teacher["token"])
    r = client.delete(
        f"{P}/courses/{dc['course']['id']}/lessons/{dc['lessons'][0].id}",
        headers=hdr(admin_token),
    )
    assert r.status_code == 204


# ============================== ENROLLMENT ==============================
def test_student_enrolls_in_published(client, student, teacher):
    pub = published_course(client, teacher["token"])
    r = client.post(
        f"{P}/courses/{pub['course']['id']}/enroll", headers=hdr(student["token"])
    )
    assert r.status_code == 200
    assert r.json()["progress"] == 0 and r.json()["completed"] is False


def test_enroll_in_draft_404(client, student, teacher):
    dc = draft_course(client, teacher["token"])
    r = client.post(
        f"{P}/courses/{dc['course']['id']}/enroll", headers=hdr(student["token"])
    )
    assert r.status_code == 404


def test_enroll_twice_403(client, student, teacher):
    pub = published_course(client, teacher["token"])
    client.post(
        f"{P}/courses/{pub['course']['id']}/enroll", headers=hdr(student["token"])
    )
    r = client.post(
        f"{P}/courses/{pub['course']['id']}/enroll", headers=hdr(student["token"])
    )
    assert r.status_code == 403


def test_teacher_cannot_enroll_in_own_course(client, teacher):
    pub = published_course(client, teacher["token"])
    r = client.post(
        f"{P}/courses/{pub['course']['id']}/enroll", headers=hdr(teacher["token"])
    )
    assert r.status_code == 403


def test_enroll_nonexistent_404(client, student):
    assert (
        client.post(
            f"{P}/courses/999999/enroll", headers=hdr(student["token"])
        ).status_code
        == 404
    )
