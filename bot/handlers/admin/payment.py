from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.crud.payment_crud import PaymentCRUD
from bot.keyboards.payment_keyboards import start_payment_keyboard
from bot.states.payment_states import PaymentProcess

router = Router(name=__name__)


@router.message()
async def start_cash_payment(message: types.Message, state: FSMContext, session: AsyncSession):
    keyboard = start_payment_keyboard
    await message.answer("Введите сумму к оплате:", reply_markup=keyboard)
    await PaymentProcess.amount.set()

@router.message(state="PaymentProcess.amount")
async def process_payment_amount(message: types.Message, state: FSMContext, session: AsyncSession):
    amount = int(message.text)
    async with state.proxy() as data:
        data["amount"] = amount
    payment_crud = PaymentCRUD()
    try:
        await payment_crud.create_cash_payment(session, data)
        await message.answer("Платеж успешно создан.")
    except ValueError as e:
        await message.answer(f"Ошибка: {e}")
    await state.finish()
