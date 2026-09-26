from pydantic import BaseModel, ConfigDict


class LessonCreate(BaseModel):
    title: str
    content: str
    video_url: str | None
    after_lesson_id: int


class LessonResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    course_id: int
    title: str
    content: str
    video_url: str | None
    order: int
    duration_minutes: int


class LessonListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    order: int
    duration_minutes: int | None
