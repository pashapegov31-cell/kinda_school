from sqlalchemy import CheckConstraint, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.schemas.base import Base


class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    course_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("courses.id"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(Text)
    video_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    order: Mapped[int] = mapped_column(Integer, name="lesson_order")
    duration_minutes: Mapped[int] = mapped_column(Integer)

    __table_args__ = (
        Index("ix_lesson_course_id", "course_id", "lesson_order"),
        CheckConstraint(
            "duration_minutes >= 0", name="ck_lessons_duration_not_negative"
        ),
    )
