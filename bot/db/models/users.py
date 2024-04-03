from sqlalchemy import Boolean, Column, Integer, String
from db.models.base import Base
from core.constants import DEFAULT_BALANCE, MAX_LENGHT_NAME_SURNAME, USER_ROLE
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from datetime import datetime
from sqlalchemy import ForeignKey

class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    phone_number: Mapped[str]
    last_name : Mapped[str] = mapped_column(String(MAX_LENGHT_NAME_SURNAME))
    first_name : Mapped[str] = mapped_column(String(MAX_LENGHT_NAME_SURNAME))
    middle_name : Mapped[str] = mapped_column(String(MAX_LENGHT_NAME_SURNAME))
    birth_date: Mapped[datetime]
    #bonus model
    bonus: Mapped[int] = mapped_column(ForeignKey('bonus.id'))
    #car model
    car: Mapped[int] = mapped_column(ForeignKey('car.id'))
    tg_user_id: Mapped[int]
    role: Mapped[str] = mapped_column(default=USER_ROLE['user'])
    is_active: Mapped[bool] = mapped_column(default=True)
    # email
    
    def __repr__(self) -> str:
        return f'ФИО {self.fio}, Номер {self.phone_number}, Роль {self.role}'
