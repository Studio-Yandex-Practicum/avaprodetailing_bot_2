from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from bot.core.enums import PaymentState
from bot.db.models.base import Base


# # FIXME: добавить cascade
# class Payment(Base):
#     __tablename__ = 'payments'

#     id: Mapped[int] = mapped_column(primary_key=True)
#     payment_type_online: Mapped[bool]
#     payment_state: Mapped[PaymentState]

#     def __repr__(self):
#         return (f'Payment(id={self.id}, online={self.payment_type_online},'
#                 f' state={self.payment_state!r})')


# TODO: не странно ли что в посещении мы регистрируем сумму, а не в платеже?
#  Если visit то же что и внесени оплаты,
#  тогда почему бы не перенести поля из Payment в Visit и сделать visit основой
class Visit(Base):
    __tablename__ = 'visits'
    # TODO: validations to constraints

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime] = mapped_column(server_default=func.now())
    summ: Mapped[int]
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
    # TODO: что за такой cars_number здесь был?
    car_id: Mapped[str] = mapped_column(ForeignKey('cars.id'))
    service_id: Mapped[Optional[int]] = mapped_column(ForeignKey('services.id'))
#    payment_id: Mapped[int] = mapped_column(ForeignKey('payments.id'))

    @validates('summ')
    def validate_positive_visit_summ(self, summ) -> int:
        if summ < 0:
            raise ValueError('Сумма платежа не может быть отрицательной.')
        return summ

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
            payment_id=obj_in['payment_id']
        )
        return db_obj
