from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.core.constants import (
    CLIENT_BIO, ERROR_MESSAGE, REF_CLIENT_INFO,
    STATE_PHONE_NUMBER, WELCOME_ADMIN_MESSAGE,
)
from bot.db.crud.users import users_crud
from bot.db.models.users import User
from bot.keyboards.admin_keyboards import (
    admin_reg_client,
    client_profile_for_adm,
    reg_or_menu_adm,
)
from bot.keyboards.super_admin_keyboards import gener_admin_keyboard
from bot.states.user_states import AdminState
from bot.utils.bonus import award_registration_bonus
from bot.utils.validators import validate_phone_number

router = Router(name=__name__)


@router.callback_query(F.data == 'switch_admin_mode')
@router.callback_query(F.data == 'admin_main_menu')
async def admin_menu(
    callback: CallbackQuery,
    session: AsyncSession,
    state: FSMContext
):
    tg_id = callback.from_user.id
    await state.clear()
    db_obj = await users_crud.get_by_attribute(
        attr_name='tg_user_id', attr_value=tg_id, session=session
    )
    await callback.message.delete()
    if db_obj.is_active:
        await callback.message.answer(
            WELCOME_ADMIN_MESSAGE,
            reply_markup=gener_admin_keyboard(db_obj.role)
        )
    await state.update_data(is_admin_menu=True)


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
    if not await validate_phone_number(phone_number=msg.text):
        await msg.delete()
        await msg.bot.edit_message_text(
            chat_id=msg.from_user.id,
            message_id=state_data['msg_id'],
            text=ERROR_MESSAGE.format(
                info_text=STATE_PHONE_NUMBER,
                incorrect=msg.text
            )
        )
        return
    await state.update_data(phone_number=msg.text)
    data = await state.get_data()
    user = await users_crud.get_by_attribute(
        session=session, attr_name='phone_number',
        attr_value=data['phone_number']
    )
    if user is None:
        await msg.bot.edit_message_text(
            text=f'Клиент с номером {data["phone_number"]} не зарегистрирован',
            chat_id=msg.from_user.id,
            message_id=state_data['msg_id'],
            reply_markup=admin_reg_client,
        )

    else:
        await msg.bot.edit_message_text(
            text=(
                CLIENT_BIO.format(
                    last_name=user.last_name,
                    first_name=user.first_name,
                    birth_date=user.birth_date,
                    balance=user.balance,
                    phone_number=user.phone_number,
                    note=user.note if user.note is not None else ''
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
    user = await users_crud.get_by_attribute(
        attr_name='phone_number',
        attr_value=state_data.get('phone_number'),
        session=session
    )
    if user is None:
        new_user = await users_crud.create(obj_in=state_data, session=session)
        bonus = await award_registration_bonus(user=new_user, session=session)
    else:
        state_data = User.update_data_to_model(db_obj=user, obj_in=state_data)
        new_user = await users_crud.update(
            db_obj=user, obj_in=state_data, session=session
        )
    await callback.bot.edit_message_text(
        text=(
            CLIENT_BIO.format(
                last_name=new_user.last_name,
                first_name=new_user.first_name,
                birth_date=new_user.birth_date,
                phone_number=new_user.phone_number,
                balance=bonus.full_amount,
                note=new_user.note if new_user.note is not None else ''
            )
        ),
        chat_id=callback.from_user.id,
        message_id=state_data['msg_id'],
        reply_markup=client_profile_for_adm,
    )
