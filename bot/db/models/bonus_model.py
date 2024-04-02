from sqlalchemy import String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import Base
from core.constants import MAX_LENGHT


class BonusesBatch(Base):
    __tablename__ = "bonuses_batch"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("id.user_id"))
    admin_id: Mapped[int] = mapped_column(ForeignKey("admin.user_id"))
    admin: Mapped["Admin"] = relationship(foreign_keys=[admin_id], back_populates="bonuses_batches")
    case_id: Mapped[int] = mapped_column(ForeignKey("case.case_id"))
    case: Mapped["BonusCase"] = relationship(back_populates="bonuses_batches")
    summ: Mapped[int]
    bonuses_start: Mapped[Date]
    time_id: Mapped[int] = mapped_column(ForeignKey("time.time_id"))
    time: Mapped["BonusTime"] = relationship(back_populates="bonuses_batches")
    bonuses_activity: Mapped[bool]

    def __repr__(self):
        return f'Клиент {self.user_id}, Колличество {self.bonuses_summ}'


class BonusCase(Base):
    __tablename__ = "bonus_case"

    id: Mapped[int] = mapped_column(primary_key=True)
    bonus_name: Mapped[str] = mapped_column(String(MAX_LENGHT))
    bonus_type: Mapped[str]

    def __repr__(self):
        return f'Название {self.bonus_name}, Тип {self.bonus_type}'


class BonusTime(Base):
    __tablename__ = "bonus_time"

    id: Mapped[int] = mapped_column(primary_key=True)
    bonus_time_day: Mapped[Date]
    bonus_time_duration: Mapped[int]

    def __repr__(self):
        return f'Дата выдачи бонуса {self.bonus_time_day}, Длительность {self.bonus_time_duration}'


class BonusPayment(Base):
    __tablename__ = "bonus_payment"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("id.user_id"))
    admin_id: Mapped[int] = mapped_column(ForeignKey("adminr.user_id"))
    admin: Mapped["Admin"] = relationship(foreign_keys=[admin_id], back_populates="bonus_payments")
    batch_id: Mapped[int] = mapped_column(ForeignKey("batch.batch_id"))
    batch: Mapped["BonusesBatch"] = relationship(back_populates="bonus_payments")
    case_id: Mapped[int] = mapped_column(ForeignKey("case.case_id"))
    case: Mapped["BonusCase"] = relationship(back_populates="bonus_payments")
    summ: Mapped[int]
    date: Mapped[Date]

    def __repr__(self):
        return f'Клиент {self.user_id_}, Списание {self.summ}'
