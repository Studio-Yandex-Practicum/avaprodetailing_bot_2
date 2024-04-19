from datetime import datetime, timedelta
from aiogram import Router, F, Bot, types
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import CallbackQuery, Message
from bot.db.crud.bonus import bonuses_crud
from bot.db.crud.cars import cars_crud
from bot.db.models import Bonus, User
from bot.db.crud.users import users_crud
from bot.core.config import settings
from bot.states.user_states import AdminState
from bot.keyboards.bonus_keyboards import (
    bonus_admin,spend_approve_cancel_keyboard,
    bonus_add_choice_keyboard, bonus_approve_cancel_keyboard,
)
from bot.db.crud.bonus import bonuses_crud

router = Router(name=__name__)


async def award_registration_bonus(user: User, session: AsyncSession):
    db_user = await users_crud.get(session=session, obj_id=user.id)
    if db_user:
        registration_bonus_amount = 100
        await bonuses_crud.create(
            obj_in={
                "user_id": user.id,
                "used_amount": 0,
                "full_amount": registration_bonus_amount,
                "start_date": datetime.now(),
                "is_active": True
            },
            session=session
        )


# использовать поле модели start_date и так же одной функцией
# async def send_bonus_expiry_reminders(session: AsyncSession):
#     current_time = datetime.now()
#     for user_id, bonus_award_time in bonus_award_times.items():
#         if (current_time - bonus_award_time) >= timedelta(days=365):
#             expiry_reminder_time = bonus_award_time + timedelta(days=365 - 14)
#             if (current_time - expiry_reminder_time) >= timedelta(days=14):
#                 message = f"Напоминаем, что через 14 дней истекает срок начисления бонуса."
#                 await send_reminder_message(user_id, message)
#
#
# # вызывать бота через ключ значение bot: Bot
# async def send_reminder_message(user_id: int, message: str):
#     bot = Bot(settings.bot_token.get_secret_value())
#     await bot.send_message(user_id, message)
#
#
# # использовать одной функцией а не разбивать на две view_bonus_history
# @router.callback_query(F.data == 'История бонусов')
# async def view_bonus_history_callback(
#     callback: CallbackQuery, session: AsyncSession
# ):
#     user_id = callback.from_user.id
#     bonus_history_messages = await view_bonus_history(user_id, session)
#     for msg in bonus_history_messages:
#         await callback.message.answer(msg)


# async def calculate_max_bonus_spend(
#     visit_amount: int, user_balance: int
# ) -> int:
#     max_percentage = 0.98
#     max_spend = int(visit_amount * max_percentage)
#     return min(max_spend, user_balance)


@router.message(AdminState.payment_amount)
async def manage_bonus_callback(
    message: types.Message, state: FSMContext, session: AsyncSession
):
    try:
        await message.delete()
        payment_amount = int(message.text)
        if payment_amount <= 0:
            raise ValueError
    except ValueError:
        await message.answer('Введите корректную положительную сумму.')
        return
    await state.update_data(payment_amount=payment_amount)
    state_data = await state.get_data()
    user = await users_crud.get_by_attribute(
        attr_name='phone_number',
        attr_value=state_data['phone_number'],
        session=session
    )
    await state.update_data(
        bonus_to_spend=min(user.balance, payment_amount * 0.98)
    )
    state_data = await state.get_data()
    await message.bot.edit_message_text(
        f"У клиента {user.balance} баллов."
        f" Может быть списано {state_data.get('bonus_to_spend')}.",
        chat_id=message.from_user.id,
        message_id=state_data['msg_id'],
        reply_markup=bonus_admin
    )


@router.callback_query(F.data == 'add_bonus')
async def add_bonus_callback(
    callback: CallbackQuery, state: FSMContext
):
    state_data = await state.get_data()
    await callback.bot.edit_message_text(
        text='Выберите сумму начисления бонуса.',
        chat_id=callback.from_user.id,
        message_id=state_data['msg_id'],
        reply_markup=bonus_add_choice_keyboard
    )


@router.callback_query(F.data.startswith('bonus_add_'))
async def process_add_bonus(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
):
    data = callback.data.split('_')[-1]
    if data in ('custom', 'sum'):
        await state.update_data(bonus_method=data)
        await state.set_state(AdminState.bonus_method)
        return
    state_data = await state.get_data()
    if not data.isdigit():
        message_text = 'Ошибка, попробуйте снова.'
    else:
        bonus_sum = state_data['payment_amount'] * int(data) // 100
        await state.update_data(bonus_to_add=bonus_sum)
        car = state_data['car']
        message_text = ('Посещение клиента:\n'
                        f'{car.brand} {car.number}\n'
                        f'{state_data["chosen_services"]}\n'
                        f'{state_data["payment_amount"]} рублей\n'
                        f'Будет начислено {bonus_sum} баллов\n')

    await callback.bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=state_data['msg_id'],
        text=message_text,
        reply_markup=bonus_approve_cancel_keyboard
    )


@router.callback_query(F.data == 'approve_bonus_add')
async def approve_bonus_callback(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession
):
    pass
    # state_data = await state.get_data()
    # await bonuses_crud.create(
    #     obj_in=
    # )


@router.callback_query(F.data == 'spend_bonus')
async def spend_bonus_callback(
    callback: CallbackQuery, session: AsyncSession, state: FSMContext
):
    state_data = await state.get_data()
    await state.set_state(AdminState.amount_bonus)
    await callback.bot.edit_message_text(
        text=f'Введите сумму списания не более {state_data.get("bonus_to_spend")}',
        chat_id=callback.from_user.id,
        message_id=state_data['msg_id'],
    )

@router.message(AdminState.amount_bonus)
async def amount_spend_bonus(message: Message, session: AsyncSession, state: FSMContext):
    if message.text.isdigit():
        state_data = await state.get_data()
        await state.update_data(amount_bonus=state_data.get('amount_bonus'))
    if 'amount_bonus' in state_data:
        user = await users_crud.get_by_attribute(
            session=session,
            attr_name='phone_number',
            attr_value=state_data.get('phone_number')
        )
        await message.bot.edit_message_text(
            text=(
                'Посещение клиента:'
                f'\n{user.cars} <Гос.номер>\n'
                f'<Список услуг посещения>\n'
                f'{state_data.get("payment_amount")} рублей\n'
                f'Будет списано {state_data.get("amount_bonus")} баллов\n\n'
                f'К оплате {state_data.get("payment_amount")-state_data.get("amount_bonus")} рублей'
            ),
            message_id=state_data.get('msg_id'),
            chat_id=message.from_user.id,
            reply_markup=spend_approve_cancel_keyboard
        )

@router.callback_query(F.data == 'cancel_spend_bonus')
async def amount_spend_bonus(message: Message, session: AsyncSession, state: FSMContext):
    state_data = await state.get_data()
    user = await users_crud.get_by_attribute(
        attr_name='phone_number',
        attr_value=state_data['phone_number'],
        session=session
    )
    
    await message.bot.edit_message_text(
        f"У клиента {user.balance} баллов."
        f" Может быть списано {state_data.get('bonus_to_spend')}.",
        chat_id=message.from_user.id,
        message_id=state_data['msg_id'],
        reply_markup=bonus_admin
    )