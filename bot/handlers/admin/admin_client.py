from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.core.constants import CLIENT_BIO
from bot.db.crud.users import users_crud
from bot.keyboards.admin_keyboards import (
    search_client_kb, admin_reg_client,
    client_profile_for_adm,
)
from bot.states.user_states import AdminState
from bot.utils.validators import validate_phone_number

router = Router(name=__name__)


@router.callback_query(F.data == 'search_client')
async def get_profile(
    callback: CallbackQuery,
    state: FSMContext,
):
    await callback.message.delete()
    await callback.message.answer(
        text='Выберите способ идентификации клиента',
        reply_markup=search_client_kb
    )
    await state.update_data(
        msg_id=callback.message.message_id
    )


@router.callback_query(F.data == 'search_phone_number')
async def get_user_by_phone(
    callback: CallbackQuery,
    state: FSMContext,
):
    await callback.message.delete()
    await state.set_state(AdminState.phone_number)

    msg = await callback.message.answer(
        text='Введите номер'
    )
    await state.update_data(
        msg_id=msg.message_id
    )
    # await callback.answer()


@router.message(AdminState.phone_number)
async def reg_phone_number(
    msg: Message,
    state: FSMContext,
    session: AsyncSession
):
    state_data = await state.get_data()
    if not await validate_phone_number(phone_number=msg.text):
        await msg.delete()
        await msg.bot.edit_message_text(
            chat_id=msg.from_user.id,
            message_id=state_data['msg_id'],
            text='неверный формат админ'
        )
        return
    await state.update_data(phone_number=msg.text)
    data = await state.get_data()
    phone_num = await users_crud.get_by_attribute(
        session=session, attr_name='phone_number',
        attr_value=data['phone_number']
    )
    if phone_num is None:
        await msg.bot.edit_message_text(
            text=f'Клиент с номером {data["phone_number"]} не зарегестрирован',
            chat_id=msg.from_user.id,
            message_id=state_data['msg_id'],
            reply_markup=admin_reg_client,
        )

    else:
        await msg.bot.edit_message_text(
            text=(
                CLIENT_BIO.format(
                    last_name=phone_num.last_name,
                    first_name=phone_num.first_name,
                    birth_date=phone_num.birth_date,
                    phone_number=phone_num.phone_number, note=phone_num.note
                )
            ),
            chat_id=msg.from_user.id,
            message_id=state_data['msg_id'],
            reply_markup=client_profile_for_adm,
        )
    await msg.delete()
