from app.entities.payment_entity import PaymentEntity


class InMemorypaymentsRepository:
    def __init__(self):
        self._payments: dict[int, PaymentEntity] = {}

    def create(self, new_payment: PaymentEntity) -> PaymentEntity:
        self._payments[new_payment.id] = new_payment
        return new_payment

    def get_by_id(self, id: int) -> PaymentEntity | None:
        return self._payments[id] or None

    def get_by_order_id(self, order_id: int) -> PaymentEntity | None:
        for payment in self._payments.values():
            if order_id == payment.order_id:
                return payment

        return None

    # ? more methods???
