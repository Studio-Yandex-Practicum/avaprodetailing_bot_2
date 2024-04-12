from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
import qrcode
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards.payment_keyboards import payment_and_bonus_menu_kb, qr_keyboard
from bot.states.payment_states import PaymentProcess

router = Router(name=__name__)


@router.callback_query(F.data == "payment_and_bonus")
async def enter_payment_and_bonus_section(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
):
    await callback.message.delete()
    await state.set_state(PaymentProcess.enter_payment)
    await callback.message.answer(
        "Меню оплаты и начисления бонусов.",
        reply_markup=payment_and_bonus_menu_kb
    )


@router.callback_query(F.data == 'scan_qr_code')
async def scan_qr_code(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.answer("Начинаю сканирование QRкода. "
                                        "Пожалуйста, приложите камеру вашего устройства к QRкоду.")


@router.callback_query(F.data == 'cancel_scan')
async def cancel_scan(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.answer("Сканирование QRкода отменено.")


@router.callback_query(F.data == 'scan_qr_code')
async def handle_scan_qr_code(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.answer("Начинаю сканирование QRкода. Пожалуйста, "
                                        "поднесите камеру вашего устройства к QRкоду.")
    await scan_qr_code(callback_query.message)
