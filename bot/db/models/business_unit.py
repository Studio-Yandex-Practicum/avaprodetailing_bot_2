from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from bot.core.constants import (MAX_LENGHT_BUSINESS_UNIT,
                                MAX_LENGHT_BUSINESS_UNIT_NOTE)
from bot.db.models.base import Base


class BusinessUnit(Base):
    __tablename__ = "business_unit"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(MAX_LENGHT_BUSINESS_UNIT))
    adress: Mapped[str] = mapped_column(String(MAX_LENGHT_BUSINESS_UNIT_NOTE))
    note: Mapped[str] = mapped_column(String(MAX_LENGHT_BUSINESS_UNIT_NOTE))
    is_active: Mapped[bool]

    def __str__(self) -> str:
        return f"Центр услуг {self.name} по адресу {self.adress}."    
