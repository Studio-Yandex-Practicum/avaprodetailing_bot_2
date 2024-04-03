import enum

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from bot.db.models.base import Base


class CarBodyTypes(str, enum.Enum):
    '''Типы кузовов (надо сделать нормальный список т.к.
        я в кузовах не разбираюсь)'''
    type1 = "Тип 1"
    type2 = "Тип 2"
    type3 = "Тип 3"


class Car(Base):
    '''Car model'''
    __tablename__ = "car"
    brand: Mapped[str] = mapped_column(String(20), nullable=False)
    model: Mapped[str] = mapped_column(String(20), nullable=False)
    number: Mapped[str] = mapped_column(String(20), unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    value: Mapped[CarBodyTypes] = mapped_column(default=CarBodyTypes.type1)

    def __repr__(self):
        return f"Брэнд-{self.brand}, Модель-{self.model}, Номер-{self.number}"
