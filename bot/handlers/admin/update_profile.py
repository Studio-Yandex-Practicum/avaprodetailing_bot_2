from datetime import datetime
from datetime import datetime as dt

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.core.constants import (BLOCK_MSG, CLIENT_BIO,
                                PROFILE_MESSAGE_WITH_INLINE, STATE_BIRTH_DATE,
                                STATE_FIO, STATE_PHONE_NUMBER, THX_REG,
                                WELCOME_ADMIN_MESSAGE)
from bot.db.crud.users import users_crud
from bot.db.models.users import User
from bot.keyboards.admin_keyboards import (add_update_data, admin_main_menu,
                                           admin_reg_client,
                                           client_profile_for_adm,
                                           reg_or_menu_adm, update_client_kb,
                                           update_profile_kb)
from bot.keyboards.users_keyboards import (add_car_kb, agree_refuse_kb,
                                           back_menu_kb, profile_kb)
from bot.states.user_states import AdminState, RegUser
from bot.utils.validators import (validate_birth_date, validate_fio,
                                  validate_phone_number)

router = Router(name=__name__)


@router.callback_query(F.data == 'update_profile')
async def update_profile_client(
    callback: CallbackQuery,
    state: FSMContext,
):
    state_data = await state.get_data()
    await callback.bot.edit_message_text(
        text=('Выберите действие'),
        chat_id=callback.from_user.id,
        message_id=state_data['msg_id'],
        reply_markup=update_profile_kb,
    )


@router.callback_query(F.data == 'update_client_data')
async def update_client_data(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession
):
    state_data = await state.get_data()
    user = await users_crud.get_by_attribute(
        session=session,
        attr_name='phone_number',
        attr_value=state_data['phone_number']
    )
    await state.update_data(
        user_id=user.id
    )
    await callback.bot.edit_message_text(
        text=(
            CLIENT_BIO.format(
                last_name=user.last_name,
                first_name=user.first_name,
                birth_date=user.birth_date,
                phone_number=user.phone_number,
                balance=user.balance,
                note=user.note
            )
        ),
        chat_id=callback.from_user.id,
        message_id=state_data['msg_id'],
        reply_markup=update_client_kb,
    )


@router.callback_query(F.data == 'update_client_fio')
async def update_client_fio(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession
):
    state_data = await state.get_data()
    await callback.bot.edit_message_text(
        text=(
            'Введите ФИО в формате Иванов Иван Иванович'
        ),
        chat_id=callback.from_user.id,
        message_id=state_data['msg_id'],
    )
    await state.set_state(AdminState.fio)


@router.message(AdminState.fio)
async def admin_update_client_fio(
    message: Message,
    state: FSMContext,
):
    state_data = await state.get_data()
    await message.delete()
    if not await validate_fio(msg=message.text):
        await message.delete()
        await message.bot.edit_message_text(
            chat_id=message.from_user.id,
            message_id=state_data['msg_id'],
            text=(
                'Введите ФИО в формате Иванов Иван Иванович'
                f'Вы ввели {message.text}'
            )
        )
        return
    await state.update_data(fio=message.text)
    await message.bot.edit_message_text(
        text=(
            f'ФИО клиента изменено на {message.text}'
        ),
        chat_id=message.from_user.id,
        message_id=state_data['msg_id'],
        reply_markup=add_update_data,
    )


@router.callback_query(F.data == 'OK_update_client')
async def update_client_data_state(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession
):
    state_data = await state.get_data()
    user = await users_crud.get_by_attribute(
        session=session,
        attr_name='phone_number',
        attr_value=state_data['phone_number']
    )
    state_data = User.update_data_to_model(db_obj=user, obj_in=state_data)
    await users_crud.update(db_obj=user, obj_in=state_data, session=session)
    
    msg = await callback.bot.edit_message_text(
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
    await state.clear()
    await state.update_data(msg_id=msg.message_id)
    await state.update_data(phone_number=user.phone_number)
    


@router.callback_query(F.data == 'update_client_birth_date')
async def update_client_birth_date(
    callback: CallbackQuery,
    state: FSMContext,
):
    state_data = await state.get_data()
    await callback.bot.edit_message_text(
        text=(
            'Введите дату рождения в формате 01.02.3000'
        ),
        chat_id=callback.from_user.id,
        message_id=state_data['msg_id'],
    )
    await state.set_state(AdminState.birth_date)


@router.message(AdminState.birth_date)
async def admin_update_client_birth_date(
    message: Message,
    state: FSMContext,
):
    state_data = await state.get_data()
    await message.delete()

    if not await validate_birth_date(msg=message.text):
        await message.delete()
        await message.bot.edit_message_text(
            chat_id=message.from_user.id,
            message_id=state_data['msg_id'],
            text=(
                'Введите дату рождения в формате 01.02.3000'
                f'Вы ввели {message.text}'
            )
        )

        return
    await state.update_data(birth_date=message.text)
    await message.bot.edit_message_text(
        text=(
            f'Дата рождения клиента изменена на {message.text}'
        ),
        chat_id=message.from_user.id,
        message_id=state_data['msg_id'],
        reply_markup=add_update_data,
    )


@router.callback_query(F.data == 'update_client_phone_number')
async def update_client_phone_number(
    callback: CallbackQuery,
    state: FSMContext,
):
    state_data = await state.get_data()
    await callback.bot.edit_message_text(
        text=(
            f'Номер телефона {state_data["phone_number"]}\n'
            'Введите новый номер телефона в формате +78888888888'
        ),
        chat_id=callback.from_user.id,
        message_id=state_data['msg_id'],
    )
    await state.set_state(AdminState.phone_num_update)


@router.message(AdminState.phone_num_update)
async def admin_update_client_phone_number(
    message: Message,
    state: FSMContext,
):
    state_data = await state.get_data()
    await message.delete()

    if not await validate_phone_number(msg=message.text):
        await message.delete()
        await message.bot.edit_message_text(
            chat_id=message.from_user.id,
            message_id=state_data['msg_id'],
            text=(
                'Введите номер телефона в формате +78888888888'
                f'Вы ввели {message.text}'
            )
        )
        return
    await state.update_data(phone_num_update=message.text)
    await message.bot.edit_message_text(
        text=(
            f'Номер телефона клиента изменена на {message.text}'
        ),
        chat_id=message.from_user.id,
        message_id=state_data['msg_id'],
        reply_markup=add_update_data,
    )


@router.callback_query(F.data == 'update_client_note')
async def update_client_note(
    callback: CallbackQuery,
    state: FSMContext,
):
    state_data = await state.get_data()
    await callback.bot.edit_message_text(
        text=(
            f'Введите комментарий к профилю клиента'
        ),
        chat_id=callback.from_user.id,
        message_id=state_data['msg_id'],
    )
    await state.set_state(AdminState.note)


@router.message(AdminState.note)
async def admin_update_client_note(
    message: Message,
    state: FSMContext,
):
    state_data = await state.get_data()
    await message.delete()
    await state.update_data(note=message.text)
    await message.bot.edit_message_text(
        text=(
            f'Комментарий к профилю клиента сохранен'
        ),
        chat_id=message.from_user.id,
        message_id=state_data['msg_id'],
        reply_markup=add_update_data,
    )


@router.callback_query(F.data == 'block_client')
async def update_client_note(
    callback: CallbackQuery,
    state: FSMContext,
):
    state_data = await state.get_data()
    await state.set_state(AdminState.reason_block)
    await callback.bot.edit_message_text(
        text=(
            f'Введите причину блокировки'
        ),
        chat_id=callback.from_user.id,
        message_id=state_data['msg_id'],
    )


@router.message(AdminState.reason_block)
async def admin_update_client_note(
    message: Message,
    state: FSMContext,
    session: AsyncSession
):
    await state.update_data(reason_block=message.text)
    state_data = await state.get_data()
    await message.delete()
    user = await users_crud.get_by_attribute(
        session=session,
        attr_name='phone_number',
        attr_value=state_data['phone_number']
    )

    await state.set_state(AdminState.approv_block)
    await message.bot.edit_message_text(
        text=(
            BLOCK_MSG.format(
                last_name=user.last_name, first_name=user.first_name,
                phone_number=user.phone_number, reason_block=state_data["reason_block"]
            )
        ),
        chat_id=message.from_user.id,
        message_id=state_data['msg_id'],
    )


@router.message(AdminState.approv_block)
async def admin_update_client_note(
    message: Message,
    state: FSMContext,
    session: AsyncSession
):
    await state.update_data(approv_block=message.text)
    state_data = await state.get_data()
    await message.delete()
    user = await users_crud.get_by_attribute(
        session=session,
        attr_name='phone_number',
        attr_value=state_data['phone_number']
    )

    if state_data['approv_block'] == 'НЕТ':
        await message.bot.edit_message_text(
            text=('Выберите действие'),
            chat_id=message.from_user.id,
            message_id=state_data['msg_id'],
            reply_markup=update_profile_kb,
        )
    elif state_data['approv_block'] == 'МЕНЮ':
        await message.bot.edit_message_text(
            WELCOME_ADMIN_MESSAGE,
            chat_id=message.from_user.id,
            message_id=state_data['msg_id'],
            reply_markup=admin_main_menu
        )
    elif state_data['approv_block'] == 'ДА':
        await message.bot.edit_message_text(
            text=(
                f'Клиент {user.last_name} {user.first_name} {user.phone_number} заблокирован '
                f'по причине {state_data["reason_block"]} '
            ),
            chat_id=message.from_user.id,
            message_id=state_data['msg_id'],
            reply_markup=add_update_data,
        )
    else:
        await message.bot.edit_message_text(
            text=(
                BLOCK_MSG.format(
                    last_name=user.last_name, first_name=user.first_name,
                    phone_number=user.phone_number, reason_block=state_data["reason_block"]
                )
            ),
            chat_id=message.from_user.id,
            message_id=state_data['msg_id'],
            reply_markup=add_update_data,
        )
