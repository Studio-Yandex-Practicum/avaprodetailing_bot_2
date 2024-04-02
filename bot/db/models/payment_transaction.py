from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship, validates

from bot.core.constatnts import PAYMENT_STATE
from bot.db.models.base import Base
from bot.db.models.users import User


class Payment(Base):
    __tablename__ = "payment"

    id: Mapped[int] = mapped_column(primary_key=True)
    payment_type_online: Mapped[bool] = mapped_column(default=False)
    payment_state: Mapped[str]

    @validates("payment_state")
    def validate_payment_state(self, payment_state):
        if payment_state not in PAYMENT_STATE:
            raise ValueError("Некорректный статус платежа.")
        self.payment_state = payment_state


class Visit(Base):
    __tablename__ = "visit"

    id: Mapped[int] = mapped_column(primary_key=True)
    visit_day: Mapped[datetime]
    business_unit_id: Mapped[int] = mapped_column(ForeignKey("business_unit.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    admin_user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    admin_user = relationship("User",
                              foreign_keys=[admin_user_id],
                              viewonly=True,
                              primaryjoin="and(Visit.admin_user_id == User.id, User.role == 'admin')")
    car_number: Mapped[str] = mapped_column(ForeignKey("car.car_number"))
    service_id: Mapped[int] = mapped_column(ForeignKey("service.id"))
    visit_summ: Mapped[int]
    payment_id: Mapped[int] = mapped_column(ForeignKey("payment.id"))
    visit_bonuspayment: Mapped[bool] = mapped_column(default=False)

    @validates("visit_summ")
    def validate_positive_visit_summ(self, visit_summ) -> int:
        if visit_summ < 0:
            raise ValueError("Сумма платежа не может быть отрицательной.")
        return visit_summ
