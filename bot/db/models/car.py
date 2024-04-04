from typing import Optional

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from bot.db.models.base import Base
from bot.core.enums import CarBodyTypes
from bot.core.constants import CAR_FIELD_LEN


class Car(Base):
    """Модель автомобиля"""

    __tablename__ = "car"
    id: Mapped[int] = mapped_column(primary_key=True)
    brand: Mapped[str] = mapped_column(String(CAR_FIELD_LEN), nullable=False)
    model: Mapped[str] = mapped_column(String(CAR_FIELD_LEN), nullable=False)
    number: Mapped[str] = mapped_column(String(CAR_FIELD_LEN), unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    car_body_type: Mapped[Optional[CarBodyTypes]]

    def __repr__(self):
        return f"Car(brand={self.brand!r}, model={self.model!r}, number={self.number!r})"
