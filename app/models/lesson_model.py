from pydantic import BaseModel


class LessonCreate(BaseModel):
    course_id: int
    title: str
    content: str
    video_url: str | None


class LessonResponse(BaseModel):
    id: int
    course_id: int
    title: str
    content: str
    video_url: str | None
    order: int
    duration_minutes: int
