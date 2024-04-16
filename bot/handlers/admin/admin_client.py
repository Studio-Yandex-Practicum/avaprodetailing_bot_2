from datetime import datetime

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.core.constants import (PROFILE_MESSAGE_WITH_INLINE, STATE_BIRTH_DATE,
                                STATE_FIO, STATE_PHONE_NUMBER, THX_REG,
                                WELCOME_ADMIN_MESSAGE, CLIENT_BIO,REF_CLIENT_INFO)
from bot.db.crud.users import users_crud
from bot.db.models.users import User
from bot.keyboards.admin_keyboards import (admin_main_menu, admin_reg_client,
                                           client_profile_for_adm,
                                           reg_or_menu_adm, search_client_kb,
                                           update_client_kb)
from bot.keyboards.users_keyboards import (add_car_kb, agree_refuse_kb,
                                           back_menu_kb, profile_kb)
from bot.states.user_states import AdminState, RegUser
from bot.utils.validators import validate_phone_number

router = Router(name=__name__)


@router.callback_query(F.data == 'admin_main_menu')
async def admin_menu(
    callback: CallbackQuery,
    session: AsyncSession,
):
    tg_id = callback.from_user.id
    db_obj = await users_crud.get_by_attribute(
        attr_name='tg_user_id', attr_value=tg_id, session=session
    )
    await callback.message.delete()
    if db_obj.is_active:
        await callback.message.answer(
            WELCOME_ADMIN_MESSAGE,
            reply_markup=admin_main_menu
        )


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
        text=STATE_PHONE_NUMBER
    )
    await state.update_data(
        msg_id=msg.message_id
    )
    await callback.answer()


@router.message(AdminState.phone_number)
async def reg_phone_number(
    msg: Message,
    state: FSMContext,
    session: AsyncSession
):
    state_data = await state.get_data()
    if not await validate_phone_number(msg=msg.text):
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
        session=session, attr_name='phone_number', attr_value=data['phone_number']
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
                    last_name=phone_num.last_name, first_name=phone_num.first_name,
                    birth_date=phone_num.birth_date,
                    phone_number=phone_num.phone_number, note=phone_num.note
                )
            ),
            chat_id=msg.from_user.id,
            message_id=state_data['msg_id'],
            reply_markup=client_profile_for_adm,
        )
    await msg.delete()


@router.callback_query(F.data == 'reg_client')
async def reg_clients(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession
):
    state_data = await state.get_data()
    await callback.bot.edit_message_text(
        text=(
            REF_CLIENT_INFO.format(phone_number=state_data["phone_number"])
        ),
        chat_id=callback.from_user.id,
        message_id=state_data['msg_id'],
        reply_markup=reg_or_menu_adm
    )


@router.callback_query(F.data == 'profile_before_search')
async def add_new_client(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession
):
    state_data = await state.get_data()
    user = await users_crud.create(obj_in=state_data, session=session)
    await callback.bot.edit_message_text(
        text=(
            CLIENT_BIO.format(
                last_name=user.last_name, first_name=user.first_name,
                birth_date=user.birth_date,
                phone_number=user.phone_number, note=user.note
            )
        ),
        chat_id=callback.from_user.id,
        message_id=state_data['msg_id'],
        reply_markup=client_profile_for_adm,
    )
