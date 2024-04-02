from sqlalchemy import Boolean, Column, Integer, String
from db.models.base import Base
from core.constants import DEFAULT_BALANCE, MAX_LENGHT_NAME_SURNAME, USER_ROLE
from sqlalchemy_utils import PhoneNumberType
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from datetime import datetime

class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    #phone_number: Mapped[PhoneNumberType]
    fio: Mapped[str] = mapped_column(String(MAX_LENGHT_NAME_SURNAME))
    birth_date: Mapped[datetime]
    #balance
    tg_user_id: Mapped[int]
    role: Mapped[str] = mapped_column(default=USER_ROLE['user'])
    # car
    # email
    
    def __repr__(self) -> str:
        return f'ФИО {self.fio}, Номер {self.phone_number}, Роль {self.role}'
