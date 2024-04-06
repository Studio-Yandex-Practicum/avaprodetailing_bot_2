from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from bot.core.enums import PaymentState
from bot.db.models.base import Base


class Payment(Base):
    __tablename__ = "payment"

    id: Mapped[int] = mapped_column(primary_key=True)
    payment_type_online: Mapped[bool]
    payment_state: Mapped[PaymentState]

    def __repr__(self):
        return (f"Payment(id={self.id}, online={self.payment_type_online},"
                f" state={self.payment_state!r})")


class Visit(Base):
    __tablename__ = "visit"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime] = mapped_column(server_default=func.now())
    summ: Mapped[int]
    bonus_payment: Mapped[bool] = mapped_column(default=False)
    # business_unit_id: Mapped[int] = mapped_column(
    #     ForeignKey("business_unit.id")
    # )
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    admin_user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    admin_user = relationship(
        "User",
        foreign_keys=[admin_user_id],
        viewonly=True,
        primaryjoin="and(Visit.admin_user_id == User.id, User.role == 'ADMIN')"
    )
    car_number: Mapped[str] = mapped_column(ForeignKey("car.number"))
    # service_id: Mapped[int] = mapped_column(ForeignKey("services.id"))
    payment_id: Mapped[int] = mapped_column(ForeignKey("payment.id"))

    @validates("summ")
    def validate_positive_visit_summ(self, summ) -> int:
        if summ < 0:
            raise ValueError("Сумма платежа не может быть отрицательной.")
        return summ

    def __repr__(self):
        return (f"Visit(id={self.id}, summ={self.summ},"
                f" date={self.date!r})")
