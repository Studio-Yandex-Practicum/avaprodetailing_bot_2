from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from bot.core.constants import DEFAULT_STRING_SIZE
from bot.core.enums import BonusType
from bot.db.models.base import Base
from bot.db.models.users import User

class Bonus(Base):
    __tablename__ = 'bonuses'
    id: Mapped[int] = mapped_column(primary_key=True)
    used_amount: Mapped[int]
    full_amount: Mapped[int]
    start_date: Mapped[datetime]
    expire_date: Mapped[datetime]
    is_active: Mapped[bool]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship(
        foreign_keys=(user_id,), back_populates='bonuses'
    )
    case_id: Mapped[Optional[int]] = mapped_column(ForeignKey('bonus_cases.id'))
    case: Mapped[Optional['BonusCase']] = relationship()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expire_date = self.start_date + timedelta(days=365)

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

class BonusHistory(Base):
    __tablename__ = 'bonus_history'
    id: Mapped[int] = mapped_column(primary_key=True)
    bonus_id: Mapped[int] = mapped_column(ForeignKey('bonuses.id'))
    amount: Mapped[int]
    date: Mapped[datetime] = mapped_column(server_default=func.now())