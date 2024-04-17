from datetime import datetime, timedelta
from typing import List
from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from bot.db.models import Bonus, User
from bot.db.crud.bonus import BonusCRUD
from bot.db.crud.users import users_crud
from bot.core.config import settings
from bot.keyboards.users_keyboards import view_bonuses, manage_bonus_keyboard

router = Router(name=__name__)


async def award_registration_bonus(user: User, session: AsyncSession):
    db_user = await users_crud.get(session=session, id=user.user_id)
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


async def calculate_max_bonus_spend(visit_amount: int, user_balance: int) -> int:
    max_percentage = 0.98
    max_spend = int(visit_amount * max_percentage)
    return min(max_spend, user_balance)


@router.callback_query(F.data.startswith('manage_bonus'))
async def manage_bonus_callback(callback: CallbackQuery, session: AsyncSession):
    action, user_id, visit_amount = callback.data.split('_')
    user_id = int(user_id)
    visit_amount = int(visit_amount)
    stmt = select(Bonus.full_amount).where(Bonus.user_id == user_id)
    result = await session.execute(stmt)
    user_balance = result.scalar_one_or_none() or 0
    max_bonus_spend = await calculate_max_bonus_spend(visit_amount, user_balance)
    await callback.message.edit_text(
        f"Посещение клиента:\n"
        f"<Марка_модель> <Гос.номер>\n"
        f"<Список услуг посещения>\n"
        f"Сумма посещения: {visit_amount} рублей\n"
        f"У клиента {user_balance} баллов.\n"
        f"Может быть списано {max_bonus_spend}.",
        reply_markup=manage_bonus_keyboard
    )


@router.callback_query(F.data.startswith('add_bonus'))
async def add_bonus_callback(callback: CallbackQuery, session: AsyncSession):
    user_id, bonus_amount = callback.data.split('_')
    user_id = int(user_id)
    bonus_amount = int(bonus_amount)
    stmt = update(Bonus).where(Bonus.user_id == user_id).values(full_amount=Bonus.full_amount + bonus_amount)
    await session.execute(stmt)
    await session.commit()
    await callback.answer("Баллы начислены!")


@router.callback_query(F.data.startswith('spend_bonus'))
async def spend_bonus_callback(callback: CallbackQuery, session: AsyncSession):
    user_id, bonus_amount = callback.data.split('_')
    user_id = int(user_id)
    bonus_amount = int(bonus_amount)
    stmt = update(Bonus).where(Bonus.user_id == user_id).values(full_amount=Bonus.full_amount - bonus_amount)
    await session.execute(stmt)
    await session.commit()
    await callback.answer("Баллы списаны!")
