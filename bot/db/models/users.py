from datetime import date
from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

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
    tg_user_id: Mapped[int]

    def __repr__(self) -> str:
        return (f'User(id={self.id}, name={self.middle_name} '
                f'{self.first_name} {self.last_name}, role={self.role})')
