from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.core.constants import WELCOME_SUPER_ADMIN_MESSAGE
from bot.db.crud.users import users_crud
from bot.keyboards.super_admin_keyboards import (admin_bio_for_super_admin_kb,
                                                 gener_list_admins,
                                                 super_admin_main_menu)

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
