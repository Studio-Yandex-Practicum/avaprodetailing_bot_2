from typing import Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from bot.core.constants import SHORT_STRING_SIZE
from bot.core.enums import CarBodyType
from bot.db.models.base import Base


class Car(Base):
    """Модель автомобиля"""

    __tablename__ = "car"
    id: Mapped[int] = mapped_column(primary_key=True)
    brand: Mapped[str] = mapped_column(String(SHORT_STRING_SIZE))
    model: Mapped[str] = mapped_column(String(SHORT_STRING_SIZE))
    number: Mapped[Optional[str]] = mapped_column(
        String(SHORT_STRING_SIZE), unique=True
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    car_body_type: Mapped[Optional[CarBodyType]]

    def __repr__(self):
        return f"Car(brand={self.brand!r}, model={self.model!r}, number={self.number!r})"
