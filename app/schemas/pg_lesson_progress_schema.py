from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.schemas.base import Base


class LessonProgress(Base):
    __tablename__ = "lesson_progresses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enrollment_id: Mapped[int] = mapped_column(Integer, ForeignKey("enrollments.id"))
    lesson_id: Mapped[int] = mapped_column(Integer, ForeignKey("lessons.id"))
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    __table_args__ = (
        UniqueConstraint(
            "enrollment_id", "lesson_id", name="uq_lesson_progress_enrollment_lesson"
        ),
        Index("ix_lesson_progress_lesson_id", "lesson_id"),
    )
