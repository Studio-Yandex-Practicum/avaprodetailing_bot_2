from typing import Optional

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from bot.db.models.base import Base
from bot.core.enums import CarBodyTypes
from bot.core.constants import (CAR_FIELD_LEN)


class Car(Base):
    '''Модель автомобиля'''
    __tablename__ = "car"
    brand: Mapped[str] = mapped_column(String(CAR_FIELD_LEN), nullable=False)
    model: Mapped[str] = mapped_column(String(CAR_FIELD_LEN), nullable=False)
    number: Mapped[str] = mapped_column(String(CAR_FIELD_LEN), unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    carbodytype: Mapped[Optional[CarBodyTypes]] = mapped_column()

    def __repr__(self):
        return f"Брэнд-{self.brand}, Модель-{self.model}, Номер-{self.number}"
