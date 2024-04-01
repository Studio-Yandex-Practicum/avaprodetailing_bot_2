from datetime import datetime
from sqlalchemy import CheckConstraint, Column, DateTime, Float, ForeignKey, Integer, String

from bot.db.models.base import Base


class PaymentTransaction(Base):
    __tablename__ = "payments_transaction"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    amount = Column(Float, CheckConstraint("amount >= 0"), nullable=False, default=0)
    bonus_amount = Column(Integer, ForeignKey("bonus.id"), CheckConstraint("bonus_amount >= 0"))
    payment_method = Column(String(10), nullable=False, default="Оплата наличными")
    payment_status = Column(String(10), nullable=False, default="Ожидание")
    reciept = Column(String(255))
    created_at = Column(DateTime, default=datetime.now())

    def __repr__(self):
        return f"{self.payment_method} | {self.payment_status} | {self.amount}"
