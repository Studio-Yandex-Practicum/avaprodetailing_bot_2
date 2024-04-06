from datetime import date, datetime

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.core.constants import DEFAULT_STRING_SIZE
from bot.db.models.base import Base

# TODO: все __repr__ в соответствующий вид
# Зачем вообще модель bonusbatch? как там может быть единый админ
# обсуждение популярных ошибок, задач, утверждение моделей
class BonusesBatch(Base):
    __tablename__ = "bonuses_batch"

    id: Mapped[int] = mapped_column(primary_key=True)

    summ: Mapped[int]
    start: Mapped[datetime]
    activity: Mapped[bool]

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(
        foreign_keys=[user_id], back_populates="bonuses_batches"
    )
    admin_user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    admin_user: Mapped["User"] = relationship(
        foreign_keys=[admin_user_id],
        back_populates="bonuses_batches",
        viewonly=True,
        primaryjoin="and(BonusesBatch.admin_user_id"
                    " == User.id, User.role == 'ADMIN')"
    )
    case_id: Mapped[int] = mapped_column(ForeignKey("bonus_case.id"))
    case: Mapped["BonusCase"] = relationship(
        foreign_keys=[case_id], back_populates="bonuses_batches"
    )
    time_id: Mapped[int] = mapped_column(ForeignKey("bonus_time.id"))
    time: Mapped["BonusTime"] = relationship(
        foreign_keys=[time_id], back_populates="bonuses_batches"
    )

    def __repr__(self):
        return f'Клиент {self.user_id}, Количество {self.summ}'


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
    day: Mapped[date] = mapped_column(server_default=func.now())
    duration: Mapped[int]

    def __repr__(self):
        return f'Дата выдачи бонуса {self.day}, Длительность {self.duration}'


class BonusPayment(Base):
    __tablename__ = "bonus_payment"

    id: Mapped[int] = mapped_column(primary_key=True)

    summ: Mapped[int]
    date: Mapped[datetime] = mapped_column(default=func.now())

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(
        foreign_keys=[user_id], back_populates="bonuses_batches"
    )
    admin_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    admin: Mapped["User"] = relationship(
        foreign_keys=[admin_id], back_populates="bonus_payments"
    )
    batch_id: Mapped[int] = mapped_column(ForeignKey("bonuses_batch.id"))
    batch: Mapped["BonusesBatch"] = relationship(
        foreign_keys=[batch_id], back_populates="bonus_payments"
    )
    case_id: Mapped[int] = mapped_column(ForeignKey("bonus_case.id"))
    case: Mapped["BonusCase"] = relationship(
        foreign_keys=[case_id], back_populates="bonus_payments"
    )

    def __repr__(self):
        return f'Клиент {self.user_id}, Списание {self.summ}'
