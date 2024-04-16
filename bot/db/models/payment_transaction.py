from datetime import datetime
from typing import Optional

from sqlalchemy import CheckConstraint, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.core.enums import PaymentState
from bot.db.models.base import Base
from bot.db.models.users import User


class Visit(Base):
    __tablename__ = 'visits'
    __table_args__ = (
        CheckConstraint("summ >= 0", name='check_summ_positive'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime] = mapped_column(server_default=func.now())
    summ: Mapped[int] = mapped_column(CheckConstraint("summ >= 0", name='check_summ_positive'))
    bonus_payment: Mapped[bool] = mapped_column(default=False)
    payment_type_online: Mapped[bool]
    payment_state: Mapped[PaymentState]
    business_unit_id: Mapped[int] = mapped_column(
        ForeignKey('business_units.id')
    )
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship(
        back_populates='visits',
        foreign_keys=(user_id,),
    )
    admin_user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    admin_user: Mapped['User'] = relationship(
        foreign_keys=(admin_user_id,)
    )
    car_id: Mapped[str] = mapped_column(ForeignKey('cars.id'))
    service_id: Mapped[Optional[int]] = mapped_column(ForeignKey('services.id'))

    def __repr__(self):
        return (f'Visit(id={self.id}, summ={self.summ},'
                f' date={self.date!r})')

    @classmethod
    def data_to_model(cls, obj_in):
        db_obj = cls(
            summ=obj_in['amount'],
            business_unit_id=obj_in['business_unit_id'],
            user_id=obj_in['user_id'],
            admin_user_id=obj_in['admin_user_id'],
        )
        return db_obj
