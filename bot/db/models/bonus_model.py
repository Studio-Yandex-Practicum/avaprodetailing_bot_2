from datetime import datetime
from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.db.models.base import Base
from bot.core.constants import DEFAULT_STRING_SIZE


class BonusesBatch(Base):
    __tablename__ = "bonuses_batch"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(foreign_keys=[user_id], back_populates="bonuses_batches")
    admin_id: Mapped[int] = mapped_column(ForeignKey("admin.admin_id"))
    admin: Mapped["Admin"] = relationship(foreign_keys=[admin_id], back_populates="bonuses_batches")
    case_id: Mapped[int] = mapped_column(ForeignKey("case.case_id"))
    case: Mapped["BonusCase"] = relationship(foreign_keys=[case_id], back_populates="bonuses_batches")
    summ: Mapped[int]
    start: Mapped[datetime]
    time_id: Mapped[int] = mapped_column(ForeignKey("time.time_id"))
    time: Mapped["BonusTime"] = relationship(foreign_keys=[time_id], back_populates="bonuses_batches")
    activity: Mapped[bool]

    def __repr__(self):
        return f'Клиент {self.user_id}, Колличество {self.summ}'


class BonusCase(Base):
    __tablename__ = "bonus_case"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(DEFAULT_STRING_SIZE))
    type: Mapped[str]

    def __repr__(self):
        return f'Название {self.name}, Тип {self.type}'


class BonusTime(Base):
    __tablename__ = "bonus_time"

    id: Mapped[int] = mapped_column(primary_key=True)
    day: Mapped[datetime] = mapped_column(default=datetime.now().date())
    duration: Mapped[int]

    def __repr__(self):
        return f'Дата выдачи бонуса {self.day}, Длительность {self.duration}'


class BonusPayment(Base):
    __tablename__ = "bonus_payment"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(foreign_keys=[user_id], back_populates="bonuses_batches")
    admin_id: Mapped[int] = mapped_column(ForeignKey("admin.admin_id"))
    admin: Mapped["Admin"] = relationship(foreign_keys=[admin_id], back_populates="bonus_payments")
    batch_id: Mapped[int] = mapped_column(ForeignKey("batch.batch_id"))
    batch: Mapped["BonusesBatch"] = relationship(foreign_keys=[batch_id], back_populates="bonus_payments")
    case_id: Mapped[int] = mapped_column(ForeignKey("case.case_id"))
    case: Mapped["BonusCase"] = relationship(foreign_keys=[case_id], back_populates="bonus_payments")
    summ: Mapped[int]
    date: Mapped[datetime]

    def __repr__(self):
        return f'Клиент {self.user_id}, Списание {self.summ}'
