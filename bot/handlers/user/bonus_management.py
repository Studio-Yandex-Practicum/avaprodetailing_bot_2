from datetime import datetime, timedelta
from typing import List
from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from bot.db.models import Bonus, User
from bot.db.crud.bonus import BonusCRUD
from bot.db.crud.users import users_crud
from bot.core.config import settings
from bot.keyboards.users_keyboards import view_bonuses

router = Router(name=__name__)



async def award_registration_bonus(user: User, session: AsyncSession):
    db_user = await users_crud.get(session=session, id=user.id)
    if db_user:
        registration_bonus_amount = 100
        bonus_crud = BonusCRUD()
        await bonus_crud.create(
            obj_in={
                "user_id": user.id,
                "used_amount": 0,
                "full_amount": registration_bonus_amount,
                "start_date": datetime.now(),
                "is_active": True
            },
            session=session
        )


@router.callback_query(F.data == 'view_balance')
async def view_balance_callback(callback: CallbackQuery, session: AsyncSession):
    user_id = callback.from_user.id
    stmt = select(Bonus.full_amount).where(Bonus.user_id == user_id)
    result = await session.execute(stmt)
    balance = result.scalar_one_or_none()

    await callback.message.answer(
        f"Ваш баланс бонусных баллов: {balance or 0}",
        reply_markup=view_bonuses 
    )

# использовать поле модели start_date и так же одной функцией
async def send_bonus_expiry_reminders(session: AsyncSession):
    current_time = datetime.now()
    for user_id, bonus_award_time in bonus_award_times.items():
        if (current_time - bonus_award_time) >= timedelta(days=365):
            expiry_reminder_time = bonus_award_time + timedelta(days=365 - 14)
            if (current_time - expiry_reminder_time) >= timedelta(days=14):
                message = f"Напоминаем, что через 14 дней истекает срок начисления бонуса."
                await send_reminder_message(user_id, message)

# вызывать бота через ключ значение bot: Bot
async def send_reminder_message(user_id: int, message: str):
    bot = Bot(settings.bot_token.get_secret_value())
    await bot.send_message(user_id, message)


# использовать одной функцией а не разбивать на две view_bonus_history
@router.callback_query(F.data == 'История бонусов')
async def view_bonus_history_callback(callback: CallbackQuery, session: AsyncSession):
    user_id = callback.from_user.id
    bonus_history_messages = await view_bonus_history(user_id, session)
    for msg in bonus_history_messages:
        await callback.message.answer(msg)

