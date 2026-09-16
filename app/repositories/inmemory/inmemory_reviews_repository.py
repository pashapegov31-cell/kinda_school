from app.entities.review_entity import ReviewEntity


class InMemoryreviewsRepository:
    def __init__(self):
        self._reviews: dict[int, ReviewEntity] = {}

    def create(self, new_review: ReviewEntity) -> ReviewEntity:
        self._reviews[new_review.id] = new_review
        return new_review

    def get_by_id(self, id: int) -> ReviewEntity | None:
        return self._reviews[id] or None

    def delete(self, data: ReviewEntity) -> ReviewEntity:
        review = self._reviews[data.id]
        if not review:
            raise Exception("Такой позиции не существует")  #! create own exceptions
        del self._reviews[review.id]
        return review

    # ? more methods???
