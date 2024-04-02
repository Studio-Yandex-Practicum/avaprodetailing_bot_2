from sqlalchemy import Column, String

from bot.db.models.base import Base


class Car(Base):
    __tablename__ = "car"
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    number = Column(String(6), unique=True)

    def __repr__(self):
        return f"Брэнд-{self.brand}, Модель-{self.model}, Номер-{self.number}"
