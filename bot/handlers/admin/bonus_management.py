from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.crud.bonus import bonuses_crud
from bot.db.crud.services import services_crud
from bot.db.crud.users import users_crud
from bot.keyboards.admin_keyboards import admin_back_kb
from bot.keyboards.bonus_keyboards import (
    bonus_add_choice_keyboard,
    bonus_admin,
    bonus_approve_amount_keyboard,
    bonus_approve_cancel_keyboard,
    spend_approve_cancel_keyboard,
)
from bot.states.user_states import AdminState
from bot.utils.bonus import spend_bonuses

router = Router(name=__name__)


@router.message(AdminState.payment_amount)
async def manage_bonus_callback(
    message: Message, state: FSMContext, session: AsyncSession
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
        bonus_to_spend=min(user.balance, int(payment_amount * 0.98))
    )
    state_data = await state.get_data()
    await message.bot.edit_message_text(
        f"У клиента {user.balance} баллов."
        f" Может быть списано {state_data['bonus_to_spend']} баллов.",
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
    state_data = await state.get_data()
    if data in ('custom', 'sum'):
        await state.update_data(bonus_method=data)
        await callback.bot.edit_message_text(
            chat_id=callback.from_user.id,
            message_id=state_data['msg_id'],
            text=f'Введите {"сумму" if data == "sum" else "процент"} бонуса'
        )
        await state.set_state(AdminState.bonus_method)
        return
    if not data.isdigit():
        await callback.bot.edit_message_text(
            chat_id=callback.from_user.id,
            message_id=state_data['msg_id'],
            text='Ошибка, попробуйте снова.'
        )
        return
    bonus_to_add = state_data['payment_amount'] * int(data) // 100
    await state.update_data(full_amount=bonus_to_add)
    car = state_data['car']
    services = []
    for service in state_data['chosen_services']:
        services.append(service)
    service_text = ','.join(services)
    await callback.bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=state_data['msg_id'],
        text=('Посещение клиента:\n'
              f'Автомобиль: {car.brand} {car.number}\n'
              f'Услуги: {service_text}\n'
              f'Сумма {state_data["payment_amount"]} рублей\n'
              f'Будет начислено {bonus_to_add} баллов\n'),
        reply_markup=bonus_approve_cancel_keyboard
    )


@router.message(AdminState.bonus_method)
async def process_bonus_method(
    message: Message,
    state: FSMContext,
    session: AsyncSession
):
    await message.delete()
    state_data = await state.get_data()
    method = state_data['bonus_method']
    if not message.text.isdigit():
        await message.bot.edit_message_text(
            message_id=state_data['msg_id'],
            chat_id=message.from_user.id,
            text='Ошибка. Попробуйте позже'
        )
        return
    amount = int(message.text)
    if method == 'sum':
        if amount > state_data['payment_amount']:
            await message.bot.edit_message_text(
                message_id=state_data['msg_id'],
                chat_id=message.from_user.id,
                text='Сумма не должна превышать сумму оплаты.'
            )
            return
        amount = int(
            amount
            / state_data['payment_amount'] * 100
        )
    await message.bot.edit_message_text(
        message_id=state_data['msg_id'],
        chat_id=message.from_user.id,
        text=f'Подтвердите процент {amount}',
        reply_markup=bonus_approve_amount_keyboard(
            f'bonus_add_{amount}'
        )
    )


@router.callback_query(F.data == 'approve_bonus_add')
async def approve_bonus_callback(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession
):
    state_data = await state.get_data()
    state_data['is_accrual'] = True
    admin_user = await users_crud.get_by_attribute(
        attr_name='tg_user_id',
        attr_value=callback.from_user.id,
        session=session
    )
    state_data['admin_user_id'] = admin_user.id
    await bonuses_crud.create(
        obj_in=state_data, session=session
    )
    await callback.bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=state_data['msg_id'],
        text=f'Начислено {state_data["full_amount"]} баллов',
        reply_markup=admin_back_kb
    )


@router.callback_query(F.data == 'spend_bonus')
async def spend_bonus_callback(
    callback: CallbackQuery, state: FSMContext
):
    state_data = await state.get_data()
    await state.set_state(AdminState.full_amount)
    await callback.bot.edit_message_text(
        text=f'Введите сумму списания не более '
             f'{state_data.get("bonus_to_spend")}',
        chat_id=callback.from_user.id,
        message_id=state_data['msg_id'],
    )


@router.message(AdminState.full_amount)
async def amount_spend_bonus(
    message: Message, session: AsyncSession, state: FSMContext
):
    await message.delete()
    state_data = await state.get_data()
    bonus_to_spend = state_data["bonus_to_spend"]
    if not (message.text.isdigit() and int(message.text) <= bonus_to_spend):
        await message.bot.edit_message_text(
            message_id=state_data.get('msg_id'),
            chat_id=message.from_user.id,
            text=f'Введите сумму целым числом не превышающим '
                 f'{bonus_to_spend}.'
        )
        return
    amount_bonus = int(message.text)
    await state.update_data(full_amount=amount_bonus)
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
            f'Будет списано {amount_bonus} баллов\n\n'
            f'К оплате {state_data["payment_amount"] - amount_bonus} рублей'
        ),
        message_id=state_data.get('msg_id'),
        chat_id=message.from_user.id,
        reply_markup=spend_approve_cancel_keyboard
    )


@router.callback_query(F.data == 'cancel_spend_bonus')
async def cancel_spend_bonus(
    message: Message, session: AsyncSession, state: FSMContext
):
    state_data = await state.get_data()
    user = await users_crud.get_by_attribute(
        attr_name='phone_number',
        attr_value=state_data['phone_number'],
        session=session
    )

    await message.bot.edit_message_text(
        f"У клиента {user.balance} баллов."
        f" Может быть списано {state_data['bonus_to_spend']}.",
        chat_id=message.from_user.id,
        message_id=state_data['msg_id'],
        reply_markup=bonus_admin
    )


@router.callback_query(F.data == 'approve_spend_bonus')
async def process_spend_bonus(
    callback: CallbackQuery, session: AsyncSession, state: FSMContext
):
    state_data = await state.get_data()
    state_data['is_accrual'] = False
    admin_user = await users_crud.get_by_attribute(
        attr_name='tg_user_id',
        attr_value=callback.from_user.id,
        session=session
    )
    state_data['admin_user_id'] = admin_user.id
    bonus_amount = state_data['full_amount']
    user = await users_crud.get(
        obj_id=state_data['user_id'], session=session
    )
    await bonuses_crud.add_multi(
        await spend_bonuses(
            list(
                filter(
                    lambda bonus: bonus.is_active and bonus.is_accrual,
                    user.bonuses
                )
            ),
            bonus_amount
        ), session=session
    )
    await bonuses_crud.create(
        obj_in=state_data, session=session
    )
    await callback.bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=state_data['msg_id'],
        text=f'Списано {state_data["full_amount"]} баллов',
        reply_markup=admin_back_kb
    )
