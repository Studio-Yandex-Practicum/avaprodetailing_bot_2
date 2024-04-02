from sqlalchemy import Integer, String
from db.models.base import Base
from core.constants import MAX_LENGHT, ZERO
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Services(Base):
    __tablename__ = 'services'
    id: Mapped[int] = mapped_column(primary_key=True)
    category: Mapped[str] = mapped_column(String(MAX_LENGHT))
    name: Mapped[str] = mapped_column(String(MAX_LENGHT))
    description: Mapped[str] = mapped_column(String(MAX_LENGHT))
    price: Mapped[int] = mapped_column(Integer, positive=True, default=ZERO)
    duration: Mapped[int] = mapped_column(Integer)
    # slug

    def __repr__(self) -> str:
        return f'Услуга {self.service},  Цена{self.price}'
