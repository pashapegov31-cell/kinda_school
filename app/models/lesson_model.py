from pydantic import BaseModel, ConfigDict


class LessonCreate(BaseModel):
    course_id: int
    title: str
    content: str
    video_url: str | None


class LessonResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    course_id: int
    title: str
    content: str
    video_url: str | None
    order: int
    duration_minutes: int
