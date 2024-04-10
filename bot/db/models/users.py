from datetime import date

from datetime import datetime as dt
from typing import Optional, cast
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


from bot.core.constants import (DEFAULT_STRING_SIZE, DEFAULT_USER_ROLE,
                                SHORT_STRING_SIZE)
from bot.core.enums import UserRole
from bot.db.models.base import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)

    is_active: Mapped[bool] = mapped_column(default=True)
    user_agreement: Mapped[bool] = mapped_column(default=True)
    role: Mapped[UserRole] = mapped_column(default=DEFAULT_USER_ROLE)
    phone_number: Mapped[str] = mapped_column(String(SHORT_STRING_SIZE))
    last_name: Mapped[str] = mapped_column(String(DEFAULT_STRING_SIZE))
    first_name: Mapped[str] = mapped_column(String(DEFAULT_STRING_SIZE))
    middle_name: Mapped[str] = mapped_column(String(DEFAULT_STRING_SIZE))
    birth_date: Mapped[date]
    note: Mapped[Optional[str]] = mapped_column(String(DEFAULT_STRING_SIZE))

    tg_user_id: Mapped[Optional[int]]

    cars: Mapped[set['Car']] = relationship()
    business_unit_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('business_units.id')
    )
    business_unit: Mapped[Optional['BusinessUnit']] = relationship(
        back_populates='admin_users'
    )
    visits: Mapped[set['Visit']] = relationship(
        back_populates='user',
        primaryjoin='User.id == Visit.user_id'
    )
    bonuses: Mapped[set['Bonus']] = relationship(
        back_populates='user',
        primaryjoin='User.id == Bonus.user_id'  # FIXME: если не будет админов
    )

    def __repr__(self) -> str:
        return (f'User(id={self.id}, name={self.middle_name} '
                f'{self.first_name} {self.last_name}, role={self.role})')

    @classmethod
    async def create_user_obj(
        self,
        obj_in,
    ):
        last_name, first_name, middle_name = [x for x in obj_in['fio'].split(' ')]
        db_obj = User(
            phone_number=obj_in['phone_number'],
            last_name=last_name,
            first_name=first_name,
            middle_name=middle_name,
            birth_date=dt.strptime(obj_in['birth_date'], '%d.%m.%Y').date(),
            tg_user_id=obj_in['tg_user_id'],
        )  # получение данных из стейтов
        return db_obj
