from datetime import date
from enum import Enum

from core.constants import MAX_LENGHT_NAME_SURNAME, PHONE_MAX_LENGTH
from db.models.base import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class UserRole(Enum):
    USER = 'Пользователь'
    ADMIN = 'Администратор'
    SUPERADMIN = 'Суперадмин'

class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    is_activity: Mapped[bool] = mapped_column(default=True)
    user_agreement: Mapped[bool] = mapped_column(default=False)
    role: Mapped[str] = mapped_column(default=UserRole.USER.value)
    
    phone_number: Mapped[str] = mapped_column(String(PHONE_MAX_LENGTH))
    last_name : Mapped[str] = mapped_column(String(MAX_LENGHT_NAME_SURNAME))
    first_name : Mapped[str] = mapped_column(String(MAX_LENGHT_NAME_SURNAME))
    middle_name : Mapped[str] = mapped_column(String(MAX_LENGHT_NAME_SURNAME))
    birth_date: Mapped[date]
    note: Mapped[str] = mapped_column(String(MAX_LENGHT_NAME_SURNAME))
    
    tg_user_id: Mapped[int]

    
    def __str__(self) -> str:
        return f'ФИО {self.fio}, Номер {self.phone_number}, Роль {self.role}'
    
    def __repr__(self) -> str:
        return f'User(id={self.id}, name={self.name}, role={self.role})'
