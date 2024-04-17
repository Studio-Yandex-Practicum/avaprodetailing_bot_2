from aiogram import F, Router
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup)
from sqlalchemy.ext.asyncio import AsyncSession
from bot.db.crud.services import services_crud
from bot.db.crud.categories import category_crud
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router(name=__name__)


@router.callback_query(F.data == 'service_catalog')
async def get_all_category(
    callback: CallbackQuery,
    session: AsyncSession,
):
    prefix = F.data.startswith('category_')

    categories = await category_crud.get_multi(session=session)
    keyboard = InlineKeyboardBuilder()

    if prefix:
        for category in categories:
            keyboard.row(InlineKeyboardButton(text=f'{category.name}',
                                              callback_data=f'{category.id}'))
    else:
        for category in categories:
            keyboard.row(InlineKeyboardButton(text=f'{category.name}',
                                              callback_data=f'{category.name}'))

    await callback.message.answer(
        text='Выберите категорию',
        reply_markup=keyboard.as_markup()
    )


@router.callback_query(F.data == 'service_catalog')
async def get_all_services(
    callback: CallbackQuery,
    session: AsyncSession,
    category_id: str,
):
    prefix = F.data.startswith('service_')

    services = await services_crud.get_by_attribute(session=session,
                                                    category_id=category_id)
    keyboard = InlineKeyboardBuilder()

    if prefix:
        for service in services:
            keyboard.row(InlineKeyboardButton(text=f'{service.note}',
                                              callback_data=f'{service.name}'))
    else:
        for service in services:
            keyboard.row(InlineKeyboardButton(text=f'{service.note}',
                                              callback_data=f'{service.id}'))

    await callback.message.answer(
        text='Выберите услугу',
        reply_markup=keyboard.as_markup()
    )

    category_id = callback.data
    service = await services_crud.get(session=session, obj_id=category_id)
    await callback.message.answer(
        callback_data=f'{service.category_id}.',
        reply_markup=InlineKeyboardMarkup().row(
            InlineKeyboardButton('Подробнее', callback_data='service_details')
        )
    )
