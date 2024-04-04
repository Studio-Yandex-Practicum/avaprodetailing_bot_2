from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship, validates

from bot.core.enums import PaymentStateEnum
from bot.db.models.base import Base


class Payment(Base):
    __tablename__ = "payment"

    id: Mapped[int] = mapped_column(primary_key=True)
    payment_type_online: Mapped[bool]
    payment_state: Mapped[str]

    @validates("payment_state")
    def validate_payment_state(self, payment_state):
        if payment_state not in PaymentStateEnum.__members__:
            raise ValueError("Некорректный статус платежа.")
        return payment_state

    def __repr__(self):
        return (f"Payment(payment_type_online={self.payment_type_online},"
                f" payment_state={self.payment_state!r})")


class Visit(Base):
    __tablename__ = "visit"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime] = mapped_column(server_default=func.now())
    summ: Mapped[int]
    bonus_payment: Mapped[bool] = mapped_column(default=False)
    business_unit_id: Mapped[int] = mapped_column(
        ForeignKey("business_unit.id")
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    admin_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    admin_user = relationship(
        "User",
        foreign_keys=[admin_user_id],
        viewonly=True,
        primaryjoin="and(Visit.admin_user_id == User.id, User.role == 'admin')"
    )
    car_number: Mapped[str] = mapped_column(ForeignKey("car.number"))
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"))
    payment_id: Mapped[int] = mapped_column(ForeignKey("payment.id"))

    @validates("summ")
    def validate_positive_visit_summ(self, summ) -> int:
        if summ < 0:
            raise ValueError("Сумма платежа не может быть отрицательной.")
        return summ

    # TODO: дописать __repr__ по аналогии с payment
