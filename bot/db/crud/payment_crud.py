from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.core.enums import PaymentState
from bot.db.models.payment_transaction import Payment, Visit
from bot.db.models.users import User


class PaymentCRUD:

    async def create_cash_payment(
        self,
        session: AsyncSession,
        obj_in,
    ) -> Payment:
        user = await session.scalar(select(User).where(User.id == obj_in["user_id"]))
        admin_user = await session.scalar(select(User).where(User.role == "ADMIN"))
        if not user:
            raise ValueError("Пользователь не найден.")
        payment_state = PaymentState.PAID if obj_in["amount"] > 0 else PaymentState.NOT_PAID
        payment = Payment(payment_type_online=False, payment_state=payment_state)
        session.add(payment)
        await session.commit()
        visit = Visit(
            date=datetime.now(),
            summ=obj_in["amount"],
            business_unit_id=user.business_unit_id,
            user_id=user.id,
            admin_user_id=admin_user.id,
            payment_id=payment.id
        )
        session.add(visit)
        await session.commit()
        return payment
        

payment_crud = PaymentCRUD()
