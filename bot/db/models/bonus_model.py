from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from db.models.base import Base
from core.constants import MAX_LENGHT


class BonusesBatch(Base):
    __tablename__ = "bonuses_batch"

    bonuses_batch_id = Column(Integer, primary_key=True)
    user_id_client = Column(Integer, ForeignKey("client.user_id"))
    user_id_admin = Column(Integer, ForeignKey("admin.user_id"))
    bonus_case_id = Column(Integer, ForeignKey("bonus_case.bonus_case_id"))
    bonus_time_id = Column(Integer, ForeignKey("bonus_time.bonus_time_id"))
    bonuses_batch_summ = Column(Integer)
    bonuses_batch_start = Column(Date)
    bonuses_batch_activity = Column(Boolean)

    client = relationship("Client", foreign_keys=[user_id_client])
    admin = relationship("Admin", foreign_keys=[user_id_admin])
    bonus_case = relationship("BonusCase")
    bonus_time = relationship("BonusTime")

    def __repr__(self):
        return f'Клиент {self.user_id_client}, Колличество {self.bonuses_batch_start}'


class BonusCase(Base):
    __tablename__ = "bonus_case"

    bonus_case_id = Column(Integer, primary_key=True)
    bonus_case_name = Column(String(MAX_LENGHT))
    bonus_case_type = Column(String)

    def __repr__(self):
        return f'Название {self.bonus_case_name}, Тип {self.bonus_case_type}'


class BonusTime(Base):
    __tablename__ = "bonus_time"

    bonus_time_id = Column(Integer, primary_key=True)
    bonus_time_day = Column(Date)
    bonus_time_duration = Column(Integer)

    def __repr__(self):
        return f'Дата выдачи бонуса {self.bonus_time_day}, Длительность {self.bonus_time_duration}'


class BonusPayment(Base):
    __tablename__ = "bonus_payment"

    bonus_payment_id = Column(Integer, primary_key=True)
    user_id_client = Column(Integer, ForeignKey("client.user_id"))
    user_id_admin = Column(Integer, ForeignKey("admin.user_id"))
    bonuses_batch_id = Column(Integer, ForeignKey("bonuses_batch.bonuses_batch_id"))
    bonus_case_id = Column(Integer, ForeignKey("bonus_case.bonus_case_id"))
    bonuses_payment_summ = Column(Integer)
    bonuses_payment_date = Column(Date)

    client = relationship("Client", foreign_keys=[user_id_client])
    admin = relationship("Admin", foreign_keys=[user_id_admin])
    bonuses_batch = relationship("BonusesBatch")
    bonus_case = relationship("BonusCase")

    def __repr__(self):
        return f'Клиент {self.user_id_client}, Списание {self.bonuses_payment_summ}'
