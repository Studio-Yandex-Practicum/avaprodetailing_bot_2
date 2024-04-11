from aiogram import Bot, F, Router, types
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.core.config import settings
from bot.db.models.users import User
from bot.keyboards.payment_keyboards import payment_method_keyboard
from bot.utils.validators import (find_user_by_phone,
                                  generate_payment_check,
                                  valid_phone_number,
                                  valid_qr_code)

bot_token = settings.bot_token
bot = Bot(token=bot_token)
router = Router(name=__name__)

@router.message(F.text == "Начало платежа.")
async def start_payment(message: types.Message, session: AsyncSession):
    user = await session.get(User, message.from_user.id)
    if user.role == "ADMIN":
        await message.answer("Отсканируйте QR-код или введите номер телефона клиента для начала оплаты.")
    else:
        await message.answer("Только администраторы могут проводить операцию оплаты работ.")

@router.message()
async def process_payment_info(message: types.Message, session: AsyncSession):
    user_input = message.text
    if valid_phone_number(user_input):
        user = await find_user_by_phone(user_input, session)
        if user:
            await process_payment(user, session)
            await message.answer("Оплата выполнена.")
        else:
            await message.answer("Пользователь не найден.")
    elif valid_qr_code(user_input):
        pass
        await message.answer("QRcode успешно отсканирован.")
    else:
        await message.answer("Неверный формат ввода. Отсканируйте QRcode или введите корректный номер телефона.")

@router.message(F.text == "Выбор способа оплаты.")
async def choose_payment_method(message: types.Message):
    keyboard = payment_method_keyboard
    await message.answer("Выберите способ оплаты.", reply_markup=keyboard)

@router.callback_query(F.text == "Оплата наличными.")
async def confirm_cash_payment(callback_query: types.CallbackQuery, session: AsyncSession):
    await callback_query.message.answer("Оплата наличными подтверждена.")
    check_file_path = generate_payment_check()
    with open(check_file_path, "rb") as check_file:
        await bot.send_document(callback_query.message.chat.id, check_file)

@router.callback_query(F.text == "Онлайн оплата.")
async def generate_payment_link(callback_query: types.CallbackQuery, session: AsyncSession, telegram_id: int):
    user = await session.scalars(select(User).where(User.tg_user_id == telegram_id))
    if user:
        pass
        payment_link = ...
        await callback_query.message.answer(f"Ссылка для онлайн оплаты: {payment_link}.")
    else:
        await callback_query.message.answer("Для онлайн оплаты нужно иметь привязку к Телеграм.")

async def process_payment(user: User, session: AsyncSession):
    await start_payment(user, session)
    services = "pass"
    bonus = "pass"
    bonus_use = "pass"
    payment_method = await choose_payment_method()
    if payment_method == "Оплата наличными.":
        await confirm_cash_payment(user, session)
    elif payment_method == "Оплата наличными.":
        await generate_payment_link(user, session)
    pass
