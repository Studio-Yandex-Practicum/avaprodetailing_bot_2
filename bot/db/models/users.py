from datetime import date
from datetime import datetime as dt
from typing import Optional, cast

from sqlalchemy import ForeignKey, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.core.constants import (
    DEFAULT_STRING_SIZE, DEFAULT_USER_ROLE,
    SHORT_STRING_SIZE,
)
from bot.core.enums import UserRole
from bot.db.models.base import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)

    is_active: Mapped[bool] = mapped_column(default=True)
    user_agreement: Mapped[bool] = mapped_column(default=True)
    role: Mapped[UserRole] = mapped_column(default=DEFAULT_USER_ROLE)
    phone_number: Mapped[str] = mapped_column(String(SHORT_STRING_SIZE))
    last_name: Mapped[Optional[str]] = mapped_column(
        String(DEFAULT_STRING_SIZE)
    )
    first_name: Mapped[Optional[str]] = mapped_column(
        String(DEFAULT_STRING_SIZE)
    )
    birth_date: Mapped[Optional[date]]
    note: Mapped[Optional[str]] = mapped_column(String(DEFAULT_STRING_SIZE))

    tg_user_id: Mapped[Optional[int]]

    cars: Mapped[set['Car']] = relationship(lazy="selectin")
    business_unit_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('business_units.id')
    )
    business_unit: Mapped[Optional['BusinessUnit']] = relationship(
        back_populates='admin_users',
        lazy='selectin'
    )
    visits: Mapped[set['Visit']] = relationship(
        back_populates='user',
        primaryjoin='User.id == Visit.user_id'
    )
    bonuses: Mapped[list['Bonus']] = relationship(
        lazy='selectin',
        order_by='Bonus.start_date',
        back_populates='user',
        primaryjoin='User.id == Bonus.user_id'
    )

    def __repr__(self) -> str:
        return (f'User(id={self.id},'
                f'{self.first_name} {self.last_name}, role={self.role})')

    @property
    def balance(self):
        # TODO: поправить relationship для пустых значений
        return sum(
            bonus.full_amount - bonus.used_amount
            for bonus in self.bonuses if bonus.is_accrual
        )

    @classmethod
    def data_to_model(
        cls,
        obj_in,
    ):
        if 'birth_date' in obj_in:
            birth_date = dt.strptime(
                obj_in.get('birth_date'), '%d.%m.%Y'
            ).date()
        else:
            birth_date = None
        if 'fio' in obj_in:
            last_name, first_name = [x for x in
                                     obj_in['fio'].split(maxsplit=1)]
            db_obj = cls(
                phone_number=obj_in['phone_number'],
                last_name=last_name,
                first_name=first_name,
                birth_date=birth_date,
                tg_user_id=obj_in.get('tg_user_id'),
                role=obj_in.get('role'),
                business_unit_id=obj_in.get('unit_id')
            )
        else:
            db_obj = cls(phone_number=obj_in['phone_number'])
        return db_obj

    @staticmethod
    def update_data_to_model(
        db_obj,
        obj_in
    ):
        if 'fio' in obj_in:
            last_name, first_name = [x for x in
                                     obj_in['fio'].split(maxsplit=1)]
            obj_in['last_name'] = last_name
            obj_in['first_name'] = first_name
        if 'birth_date' in obj_in:
            obj_in['birth_date'] = dt.strptime(
                obj_in['birth_date'], '%d.%m.%Y'
            ).date()
        if 'phone_num_update' in obj_in:
            obj_in['phone_number'] = obj_in['phone_num_update']
        if 'note' in obj_in:
            if db_obj.note is not None:
                obj_in['note'] = db_obj.note + '\n' + obj_in['note']
        if 'reason_block' in obj_in:
            obj_in['note'] = obj_in['reason_block']
            obj_in['is_active'] = False
        if 'unit_id' in obj_in:
            obj_in['business_unit_id'] = obj_in['unit_id']
        return obj_in
