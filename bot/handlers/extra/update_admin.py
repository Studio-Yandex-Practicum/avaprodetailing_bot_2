from datetime import datetime

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession
from bot.db.crud.business_units import business_units_crud
from bot.core.constants import (CLIENT_BIO, PROFILE_MESSAGE_WITH_INLINE,
                                REF_CLIENT_INFO, STATE_BIRTH_DATE, STATE_FIO,
                                STATE_PHONE_NUMBER, THX_REG,
                                WELCOME_ADMIN_MESSAGE,
                                WELCOME_SUPER_ADMIN_MESSAGE)
from bot.core.enums import UserRole
from bot.db.crud.users import users_crud
from bot.db.models.users import User
from bot.keyboards.admin_keyboards import (admin_main_menu, admin_reg_client,
                                           client_profile_for_adm,
                                           reg_or_menu_adm, update_client_kb)
from bot.keyboards.super_admin_keyboards import (OK_add_admin,
                                                 gener_admin_keyboard,
                                                 role_for_admin_kb,gener_business_unit_for_admin,
                                                 super_admin_main_menu)
from bot.keyboards.users_keyboards import (add_car_kb, agree_refuse_kb,
                                           back_menu_kb, profile_kb)
from bot.states.user_states import AdminState, RegUser, SuperAdminState
from bot.utils.validators import validate_phone_number

router = Router(name=__name__)


@router.callback_query(F.data == 'reg_new_admin')
async def reg_new_admin(
    callback: CallbackQuery,
    session: AsyncSession,
    state: FSMContext
):
    state_data = await state.get_data()
    await state.set_state(SuperAdminState.phone_number)
    await callback.bot.edit_message_text(
        text='Введите номер телефона в формате +78888888888',
        chat_id=callback.from_user.id,
        message_id=state_data['msg_id']
    )


@router.message(SuperAdminState.phone_number)
async def reg_super_admin_phone(
    msg: Message,
    state: FSMContext,
    session: AsyncSession
):
    await msg.delete()
    await state.update_data(phone_number=msg.text)
    state_data = await state.get_data()
    await state.set_state(SuperAdminState.fio)
    await msg.bot.edit_message_text(
        text='Введите ФИО в формате Иванов Иван Иванович',
        chat_id=msg.from_user.id,
        message_id=state_data['msg_id'],
    )


@router.message(SuperAdminState.fio)
async def reg_super_admin_phone(
    msg: Message,
    state: FSMContext,
    session: AsyncSession
):
    await msg.delete()
    await state.update_data(fio=msg.text)
    state_data = await state.get_data()
    await msg.bot.edit_message_text(
        text=(
            'Вы регистрируете администратора с данными:'
            f'\nФИО {state_data["fio"]}\n'
            f'Номер телефона {state_data["phone_number"]}\n\n'
            'Укажите уровень прав'
        ),
        chat_id=msg.from_user.id,
        message_id=state_data['msg_id'],
        reply_markup=role_for_admin_kb
    )
    

@router.callback_query(F.data == 'give_super_admin_permissions')
async def give_super_admin_permissions(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
):
    state_data = await state.get_data()
    await callback.bot.edit_message_text(
        text=(
            'Вы регистрируете администратора с данными:'
            f'\nФИО {state_data["fio"]}\n'
            f'Номер телефона {state_data["phone_number"]}\n\n'
            f'{UserRole.SUPERADMIN}'
        ),
        chat_id=callback.from_user.id,
        message_id=state_data['msg_id'],
        reply_markup=OK_add_admin
    )
    await state.update_data(role=UserRole.SUPERADMIN)
    

@router.callback_query(F.data == 'give_admin_permissions')
async def give_admin_permissions(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
):
    state_data = await state.get_data()
    units = await business_units_crud.get_multi(session=session)
    await callback.bot.edit_message_text(
        text=(
            'Выберите бизнес-юнит администратора'
        ),
        chat_id=callback.from_user.id,
        message_id=state_data['msg_id'],
        reply_markup=gener_business_unit_for_admin(units)
    )
    await state.update_data(role=UserRole.ADMIN)


@router.callback_query(F.data.startswith('add_unit_admin_'))
async def process_selected_business_unit(
    callback_query: CallbackQuery,
    state: FSMContext,
    session: AsyncSession
):
    unit = await business_units_crud.get(
        obj_id=int(callback_query.data.split('_')[-1]), session=session
    )
    
    
    await state.update_data(unit_id=unit.id)
    state_data = await state.get_data()
    await users_crud.create(obj_in=state_data,session=session)
    


@router.callback_query(F.data == 'invite_admin')
async def invite_admin(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
):
    await callback.message.delete()
    state_data = await state.get_data()
    await users_crud.create(obj_in=state_data,session=session)
    await callback.bot.edit_message_text(
        text=(
            '/start'
        ),
        chat_id=callback.from_user.id,
        message_id=state_data['msg_id'],
    ) 
    
    
    

    