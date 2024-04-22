from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.crud.business_units import business_units_crud
from bot.keyboards.business_units_keyboards import (
    build_business_units_keyboard, business_unit_edit_keyboard,
    business_unit_manage_keyboard)
from bot.keyboards.super_admin_keyboards import super_admin_back_kb
from bot.states.user_states import BusinessUnitState

router = Router(name=__name__)

BUSINESS_UNIT_INFO = (
    'Информация о бизнес-юните\n'
    'Название: {name}\n'
    'Описание {note}\n'
    'Адрес: {address}\n'
    'Статус: {status}'
)


@router.callback_query(F.data == 'business_units')
async def business_units_management(
    callback_query: CallbackQuery,
    state: FSMContext,
    session: AsyncSession
):
    units = await business_units_crud.get_multi(session=session)
    await callback_query.message.delete()
    msg = await callback_query.message.answer(
        text='Управление бизнес-юнитами',
        reply_markup=build_business_units_keyboard(units)
    )
    await state.update_data(msg_id=msg.message_id)


@router.callback_query(F.data == 'create_business_unit')
async def create_business_unit(
    callback_query: CallbackQuery,
    state: FSMContext,
):
    state_data = await state.get_data()
    await state.set_state(BusinessUnitState.name)
    await callback_query.message.bot.edit_message_text(
        chat_id=callback_query.from_user.id,
        message_id=state_data['msg_id'],
        text='Внесите название нового Бизнес-юнита',
    )


@router.message(BusinessUnitState.name)
async def process_name(
    message: Message,
    state: FSMContext
):
    await message.delete()
    await state.update_data(name=message.text)
    state_data = await state.get_data()
    await state.set_state(BusinessUnitState.note)
    await message.bot.edit_message_text(
        chat_id=message.from_user.id,
        message_id=state_data['msg_id'],
        text='Внесите описание нового Бизнес-юнита'
    )


@router.message(BusinessUnitState.note)
async def process_description(
    message: Message,
    state: FSMContext
):
    await message.delete()
    await state.update_data(note=message.text)
    state_data = await state.get_data()
    await message.bot.edit_message_text(
        chat_id=message.from_user.id,
        message_id=state_data['msg_id'],
        text='Внесите адрес нового Бизнес-юнита'
    )
    await state.set_state(BusinessUnitState.address)


@router.message(BusinessUnitState.address)
async def process_address(
    message: Message,
    state: FSMContext,
    session: AsyncSession
):
    await message.delete()
    data = await state.get_data()
    data['address'] = message.text
    created_obj = await business_units_crud.create(
        obj_in=data, session=session
    )
    await message.bot.edit_message_text(
        chat_id=message.from_user.id,
        message_id=data['msg_id'],
        text=('Создан новый Бизнес-юнит:\n'
              f'Название: {created_obj.name}\n'
              f'Описание: {created_obj.note}\n'
              f'Адрес: {created_obj.address}'),
        reply_markup=super_admin_back_kb
    )


@router.callback_query(F.data.startswith('business_unit_'))
async def process_selected_business_unit(
    callback_query: CallbackQuery,
    state: FSMContext,
    session: AsyncSession
):
    unit = await business_units_crud.get(
        obj_id=int(callback_query.data.split('_')[-1]), session=session
    )
    state_data = await state.get_data()
    await state.update_data(unit_id=unit.id)
    await callback_query.bot.edit_message_text(
        chat_id=callback_query.from_user.id,
        message_id=state_data['msg_id'],
        text=BUSINESS_UNIT_INFO.format(
            name=unit.name,
            note=unit.note,
            address=unit.address,
            status="Активен" if unit.is_active else "Неактивен"
        ),
        reply_markup=business_unit_manage_keyboard(unit.is_active)
    )


@router.callback_query(F.data == 'edit_unit')
async def process_edit_unit_menu(
    callback_query: CallbackQuery,
    state: FSMContext
):
    state_data = await state.get_data()
    await callback_query.bot.edit_message_text(
        chat_id=callback_query.from_user.id,
        message_id=state_data['msg_id'],
        text='Выберите поле для редактирования',
        reply_markup=business_unit_edit_keyboard
    )


@router.callback_query(F.data.startswith('edit_unit_'))
async def process_edit_unit_data(
    callback_query: CallbackQuery,
    state: FSMContext
):
    field = callback_query.data.split('_')[-1]
    state_data = await state.get_data()
    await state.update_data(edit_field=field)
    replies = {
        'name': 'Введите новое название',
        'address': 'Введите новый адрес',
        'note': 'Введите новое описание'
    }
    if field == 'status':
        message_text = 'Для изменения статуса бизнес-юнита введите ДА'
    else:
        message_text = replies[field]
    await callback_query.bot.edit_message_text(
        chat_id=callback_query.from_user.id,
        message_id=state_data['msg_id'],
        text=message_text,
    )
    await state.set_state(BusinessUnitState.edit_field)


@router.message(BusinessUnitState.edit_field)
async def process_edit_fields(
    message: Message,
    state: FSMContext,
    session: AsyncSession
):
    await message.delete()
    state_data = await state.get_data()
    unit = await business_units_crud.get(
        obj_id=state_data['unit_id'], session=session
    )
    field = state_data['edit_field']
    if field == 'status' and message.text == 'ДА':
        await business_units_crud.update(
            db_obj=unit, obj_in={
                'is_active': not unit.is_active
            }, session=session
        )

    if field != 'status':
        await business_units_crud.update(
            db_obj=unit, obj_in={
                field: message.text
            }, session=session
        )

    await message.bot.edit_message_text(
        chat_id=message.from_user.id,
        message_id=state_data['msg_id'],
        text=BUSINESS_UNIT_INFO.format(
            name=unit.name,
            note=unit.note,
            address=unit.address,
            status="Активен" if unit.is_active else "Неактивен"
        ),
        reply_markup=business_unit_manage_keyboard(unit.is_active)
    )
