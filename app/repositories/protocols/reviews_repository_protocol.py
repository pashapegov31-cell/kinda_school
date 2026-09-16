from typing import Protocol

from app.entities.review_entity import ReviewEntity


class ReviewsRepository(Protocol):
    async def create(self, new_review: ReviewEntity) -> ReviewEntity: ...
    async def get_by_id(self, id: int) -> ReviewEntity | None: ...
