from datetime import datetime

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession
from bot.core.constants import (PROFILE_MESSAGE_WITH_INLINE, STATE_BIRTH_DATE,
                                STATE_FIO, STATE_PHONE_NUMBER, THX_REG,
                                WELCOME_ADMIN_MESSAGE, CLIENT_BIO,REF_CLIENT_INFO, WELCOME_SUPER_ADMIN_MESSAGE)
from bot.core.enums import UserRole
from bot.db.crud.users import users_crud
from bot.db.models.users import User
from bot.keyboards.admin_keyboards import (admin_main_menu, admin_reg_client,
                                           client_profile_for_adm,
                                           reg_or_menu_adm,
                                           update_client_kb)
from bot.keyboards.super_admin_keyboards import admin_bio_for_super_admin_kb, gener_admin_keyboard, gener_list_admins, super_admin_main_menu
from bot.keyboards.users_keyboards import (add_car_kb, agree_refuse_kb,
                                           back_menu_kb, profile_kb)
from bot.states.user_states import AdminState, RegUser, SuperAdminState
from bot.utils.validators import validate_phone_number

router = Router(name=__name__)






@router.callback_query(F.data == 'extra_admin')
async def super_admin_menu(
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
    await state.update_data(
        msg_id=callback.message.message_id
    )
    if db_obj.is_active:
        msg = await callback.message.answer(
                WELCOME_SUPER_ADMIN_MESSAGE,
                reply_markup=super_admin_main_menu
            )
        await state.update_data(
        msg_id=msg.message_id
    )




@router.callback_query(F.data == 'administrators')
async def get_admins_list(
    callback: CallbackQuery,
    session: AsyncSession,
    state: FSMContext
):
    admins = await users_crud.get_multi(session=session)
    await callback.message.delete()
    msg = await callback.message.answer(
        text='Выберите админа',
        reply_markup=gener_list_admins(admins)
    )
    await state.update_data(msg_id=msg.message_id)
    
    
    

    
    

@router.callback_query(F.data.startswith('admin_bio_'))
async def process_selected_business_unit(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession
):
    admin = await users_crud.get(
        obj_id=int(callback.data.split('_')[-1]), session=session
    )
    await state.update_data(admin_id=admin.id)
    state_data = await state.get_data()
    await callback.bot.edit_message_text(
        text=(
            'Выберите действие для администратора:'
            f'\nФИО {admin.last_name} {admin.first_name}\n'
            f'Номер телефона {admin.phone_number}\n'
            f'{admin.role}\n'
            f'{admin.business_unit}\n'
            f'{"Действующий" if admin.is_active else "Архив"}'
        ),
        chat_id=callback.from_user.id,
        message_id=state_data['msg_id'],
        reply_markup=admin_bio_for_super_admin_kb(admin.is_active)
    )