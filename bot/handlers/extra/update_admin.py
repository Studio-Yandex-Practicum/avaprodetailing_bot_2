from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.core.constants import (
    ERROR_MESSAGE,
    STATE_FIO,
    STATE_PHONE_NUMBER,
    WELCOME_SUPER_ADMIN_MESSAGE,
)
from bot.core.enums import UserRole
from bot.db.crud.business_units import business_units_crud
from bot.db.crud.users import users_crud
from bot.db.models.users import User
from bot.keyboards.super_admin_keyboards import (
    OK_add_admin,
    gener_business_unit_for_admin,
    ok_admin_bio,
    role_for_admin_kb,
    super_admin_main_menu,
)
from bot.states.user_states import SuperAdminState
from bot.utils.validators import validate_fio, validate_phone_number

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
    state_data = await state.get_data()
    if 'change_phone_num' not in state_data:
        await state.set_state(SuperAdminState.fio)
        await msg.bot.edit_message_text(
            text='Введите ФИО в формате Иванов Иван Иванович',
            chat_id=msg.from_user.id,
            message_id=state_data['msg_id'],
        )
        return
    admin = await users_crud.get(
        session=session, obj_id=state_data['admin_id']
    )
    state_data = User.update_data_to_model(db_obj=admin, obj_in=state_data)
    admin11 = await users_crud.update(
        db_obj=admin, obj_in=state_data, session=session
    )
    await msg.bot.edit_message_text(
        f'Номер телефона изменен {state_data["phone_number"]}',
        reply_markup=ok_admin_bio(admin11),
        chat_id=msg.from_user.id,
        message_id=state_data['msg_id'],
    )


@router.message(SuperAdminState.fio)
async def reg_super_admin_fio(
    msg: Message,
    state: FSMContext,
    session: AsyncSession
):
    await msg.delete()
    state_data = await state.get_data()
    if not await validate_fio(msg=msg.text):
        await msg.delete()
        await msg.bot.edit_message_text(
            chat_id=msg.from_user.id,
            message_id=state_data['msg_id'],
            text=ERROR_MESSAGE.format(
                info_text=STATE_FIO,
                incorrect=msg.text
            )
        )
        return
    await state.update_data(fio=msg.text)
    state_data = await state.get_data()
    if 'change_fio' not in state_data:
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
        return
    admin = await users_crud.get(
        session=session, obj_id=state_data.get('admin_id')
    )
    state_data = User.update_data_to_model(db_obj=admin, obj_in=state_data)
    admin11 = await users_crud.update(
        db_obj=admin, obj_in=state_data, session=session
    )
    await msg.bot.edit_message_text(
        f'ФИО изменено на {state_data["fio"]}',
        reply_markup=ok_admin_bio(admin11),
        chat_id=msg.from_user.id,
        message_id=state_data['msg_id'],
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
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession
):
    unit = await business_units_crud.get(
        obj_id=int(callback.data.split('_')[-1]), session=session
    )
    await state.update_data(unit_id=unit.id)
    state_data = await state.get_data()
    if 'change_unit' not in state_data:
        await callback.bot.edit_message_text(
            text=(
                'Вы регистрируете администратора с данными:'
                f'\nФИО {state_data["fio"]}\n'
                f'Номер телефона {state_data["phone_number"]}\n\n'
                f'{UserRole.ADMIN}'
            ),
            chat_id=callback.from_user.id,
            message_id=state_data['msg_id'],
            reply_markup=OK_add_admin
        )
        return
    admin = await users_crud.get(
        session=session, obj_id=state_data['admin_id']
    )
    state_data = User.update_data_to_model(db_obj=admin, obj_in=state_data)
    admin11 = await users_crud.update(
        db_obj=admin, obj_in=state_data, session=session
    )
    await callback.bot.edit_message_text(
        f'Бизнес-юнит изменен на {state_data["unit_id"]}',
        reply_markup=ok_admin_bio(admin11),
        chat_id=callback.from_user.id,
        message_id=state_data['msg_id'],
    )


@router.callback_query(F.data == 'invite_admin')
async def invite_admin(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
):

    state_data = await state.get_data()
    admin = await users_crud.get_by_attribute(
        session=session,
        attr_name='phone_number',
        attr_value=state_data.get('phone_number')
        
    )

    if admin is None:
        admin = await users_crud.create(
            obj_in=state_data, session=session
        )
        await award_registration_bonus(admin, session)
    else:
        state_data = User.update_data_to_model(db_obj=admin, obj_in=state_data)
        admin = await users_crud.update(
            db_obj=admin, obj_in=state_data, session=session
        )
    await callback.bot.edit_message_text(
        WELCOME_SUPER_ADMIN_MESSAGE,
        reply_markup=super_admin_main_menu,
        chat_id=callback.from_user.id,
        message_id=state_data['msg_id'],
    )
    await state.clear()


@router.callback_query(F.data == 'block_admin')
async def block_admin(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
):
    state_data = await state.get_data()
    admin = await users_crud.get(
        session=session, obj_id=state_data['admin_id']
    )
    state_data['is_active'] = not admin.is_active
    admin = await users_crud.update(
        db_obj=admin, obj_in=state_data, session=session
    )
    await callback.bot.edit_message_text(
        'Статус администратора изменен на '
        f'{"Действующий" if admin.is_active else "Архив"}',
        reply_markup=ok_admin_bio(admin),
        chat_id=callback.from_user.id,
        message_id=state_data['msg_id'],
    )


@router.callback_query(F.data == 'change_role')
async def change_role(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
):
    state_data = await state.get_data()
    admin = await users_crud.get(
        session=session, obj_id=state_data['admin_id']
    )
    state_data['role'] = (UserRole.SUPERADMIN
                          if admin.role is UserRole.ADMIN else UserRole.ADMIN)
    admin = await users_crud.update(
        db_obj=admin, obj_in=state_data, session=session
    )
    old_role = ("Администратор"
                if admin.role is UserRole.SUPERADMIN
                else "Старший администратор")
    new_role = ("Администратор"
                if admin.role is UserRole.ADMIN
                else "Старший администратор")
    await callback.bot.edit_message_text(
        f'Роль {old_role} изменена на {new_role}',
        reply_markup=ok_admin_bio(admin),
        chat_id=callback.from_user.id,
        message_id=state_data['msg_id'],
    )


@router.callback_query(F.data == 'change_business_unit')
async def change_business_unit(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
):
    state_data = await state.get_data()
    units = await business_units_crud.get_multi(session=session)
    await state.update_data(change_unit=True)
    await callback.bot.edit_message_text(
        text=(
            'Выберите бизнес-юнит администратора'
        ),
        chat_id=callback.from_user.id,
        message_id=state_data['msg_id'],
        reply_markup=gener_business_unit_for_admin(units)
    )


@router.callback_query(F.data == 'change_phone_number_admin')
async def change_phone_number_admin(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
):
    state_data = await state.get_data()
    await state.update_data(change_phone_num=True)
    await state.set_state(SuperAdminState.phone_number)
    await callback.bot.edit_message_text(
        text=(
            'Введите номер телефона в формате +78888888888'
        ),
        chat_id=callback.from_user.id,
        message_id=state_data['msg_id'],
    )


@router.callback_query(F.data == 'change_phone_fio')
async def change_phone_fio(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
):
    state_data = await state.get_data()
    await state.update_data(change_fio=True)
    await state.set_state(SuperAdminState.fio)
    await callback.bot.edit_message_text(
        text=(
            'Введите ФИО в формате Иванов Иван Иванович'
        ),
        chat_id=callback.from_user.id,
        message_id=state_data['msg_id'],
    )
