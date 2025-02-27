from datetime import datetime

from sqlalchemy import CheckConstraint, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.core.constants import PAID
from bot.core.enums import PaymentState
from bot.db.models.base import Base


class Visit(Base):
    __tablename__ = 'visits'
    __table_args__ = (
        CheckConstraint("summ >= 0", name='check_summ_positive'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime] = mapped_column(server_default=func.now())
    summ: Mapped[int]
    payment_type_online: Mapped[bool] = mapped_column(default=False)
    payment_state: Mapped[PaymentState] = mapped_column(default=PAID)
    business_unit_id: Mapped[int] = mapped_column(
        ForeignKey('business_units.id')
    )
    business_unit: Mapped['BusinessUnit'] = relationship(
        foreign_keys=(business_unit_id,), lazy='selectin'
    )
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship(
        back_populates='visits',
        foreign_keys=(user_id,),
    )
    admin_user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    admin_user: Mapped['User'] = relationship(
        foreign_keys=(admin_user_id,), lazy='selectin'
    )
    car_id: Mapped[str] = mapped_column(ForeignKey('cars.id'))
    services: Mapped[str]

    def __repr__(self):
        return (f'Visit(id={self.id}, summ={self.summ},'
                f' date={self.date!r})')

    @classmethod
    def data_to_model(cls, obj_in):
        db_obj = cls(
            summ=obj_in['payment_amount'],
            business_unit_id=obj_in['business_unit_id'],
            user_id=obj_in['user_id'],
            admin_user_id=obj_in['admin_user_id'],
            car_id=obj_in['car'].id,
            services=obj_in['chosen_services']
        )
        return db_obj
