from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.core.constants import DEFAULT_STRING_SIZE
from bot.core.enums import BonusType
from bot.db.models.base import Base


class Bonus(Base):
    __tablename__ = 'bonuses'

    id: Mapped[int] = mapped_column(primary_key=True)

    used_amount: Mapped[int]
    full_amount: Mapped[int]
    start_date: Mapped[datetime]
    is_active: Mapped[bool]

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship(
        foreign_keys=(user_id,), back_populates='bonuses'
    )
    admin_user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    case_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('bonus_cases.id')
    )
    case: Mapped[Optional['BonusCase']] = relationship()

    def __repr__(self):
        return (f'Bonus(id={self.id}, '
                f'remaining={self.full_amount - self.used_amount})')


class BonusCase(Base):
    __tablename__ = 'bonus_cases'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(DEFAULT_STRING_SIZE))
    type: Mapped[BonusType]
    amount: Mapped[Optional[int]]

    def __repr__(self):
        return (f'BonusCase(name={self.name}, type={self.type},'
                f' amount={self.amount})')
