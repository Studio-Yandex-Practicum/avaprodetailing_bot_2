from aiogram import F, Router
from aiogram.types import (
    CallbackQuery, InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.crud.categories import category_crud
from bot.db.crud.services import services_crud
from bot.keyboards.users_keyboards import gener_service_kb
from aiogram.fsm.context import FSMContext

router = Router(name=__name__)


@router.callback_query(F.data == 'service_catalog')
async def get_all_category(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession
):
    await callback.message.delete()
    categories = await category_crud.get_multi(session=session)
    keyboard = InlineKeyboardBuilder()
    for category in categories:
        if category.is_active:
            keyboard.row(
                InlineKeyboardButton(
                    text=f'{category.name}',
                    callback_data=f'categories_from_service_{category.id}'
                )
            )
    keyboard.row(
        InlineKeyboardButton(
            text='Выход в меню',
            callback_data='menu'
        )
    )
    msg = await callback.message.answer(
        text='Выберите категорию',
        reply_markup=keyboard.as_markup(),
    )
    await state.update_data(msg_id=msg.message_id)


@router.callback_query(F.data.startswith('categories_from_service_'))
async def get_all_services(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession
):
    state_data = await state.get_data()
    category = await category_crud.get(
        obj_id=int(callback.data.split('_')[-1]), session=session
    )
    services = category.services
    await state.update_data(cat_id=category.id)
    await callback.bot.edit_message_text(
        text='Выберите услугу',
        chat_id=callback.from_user.id,
        message_id=state_data.get('msg_id'),
        reply_markup=gener_service_kb(services)
    )


@router.callback_query(F.data.startswith('services_from_BU_'))
async def get_all_services_business_unit(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession
):
    service = await services_crud.get(
        obj_id=int(callback.data.split('_')[-1]), session=session
    )
    state_data = await state.get_data()
    msg = f'Услуга "{service.name}" может быть оказана в:\n\n'
    for bu in service.business_units:
        msg += f'{bu.name} по адресу {bu.address}\n\n'
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(
            text='Вернуться к списку услуг',
            callback_data=f'categories_from_service_{state_data["cat_id"]}'
        )
        ]]
    )

    await callback.bot.edit_message_text(
        text=msg,
        chat_id=callback.from_user.id,
        message_id=state_data.get('msg_id'),
        reply_markup=keyboard
    )
