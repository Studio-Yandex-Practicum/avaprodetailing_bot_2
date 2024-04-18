from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.core.constants import DEFAULT_STRING_SIZE
from bot.core.enums import BonusType
from bot.db.models.base import Base


class Bonus(Base):
    __tablename__ = 'bonuses'

    id: Mapped[int] = mapped_column(primary_key=True)

    used_amount: Mapped[int] = mapped_column(default=0)
    full_amount: Mapped[int]
    start_date: Mapped[datetime] = mapped_column(server_default=func.now())
    is_active: Mapped[bool] = mapped_column(default=True)
    is_accrual: Mapped[bool]

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship(
        foreign_keys=(user_id,), back_populates='bonuses'
    )
    admin_user_id: Mapped[Optional[int]] = mapped_column(ForeignKey('users.id'))
    admin_user: Mapped[Optional['User']] = relationship(
        foreign_keys=(admin_user_id,),
        back_populates='bonuses',
        viewonly=True,
        primaryjoin='and_(Bonus.admin_user_id'
                    ' == User.id, User.role == "ADMIN")'
    )
    case_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('bonus_cases.id')
    )
    case: Mapped[Optional['BonusCase']] = relationship()
    
    @classmethod
    def data_to_model(cls, data):
        return cls(
            used_amount=data.get('used_amount'),
            full_amount=data.get('full_amount'),
            user_id=data.get('user_id')
        )

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
