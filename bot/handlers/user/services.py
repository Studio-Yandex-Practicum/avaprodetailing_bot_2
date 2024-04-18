from aiogram import F, Router
from aiogram.types import CallbackQuery, InlineKeyboardButton
from sqlalchemy.ext.asyncio import AsyncSession
from bot.db.crud.services import services_crud
from bot.db.crud.categories import category_crud
from bot.db.crud.business_units import business_units_crud
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router(name=__name__)


@router.callback_query(F.data == 'service_catalog')
async def get_all_category(
    callback: CallbackQuery,
    session: AsyncSession,
):
    categories = await category_crud.get_multi(session=session)
    keyboard = InlineKeyboardBuilder()
    for category in categories:
        if category.is_active:
            keyboard.row(InlineKeyboardButton(text=f'{category.name}',
                                              callback_data=f'categories_from_service_{category.id}'))
    await callback.message.answer(
        text='Выберите категорию',
        reply_markup=keyboard.as_markup()
    )
    await callback.message.delete()


@router.callback_query(F.data.startswith('categories_from_service_'))
async def get_all_services(
    callback: CallbackQuery,
    session: AsyncSession
):
    category = await category_crud.get(
        obj_id=int(callback.data.split('_')[-1]), session=session
    )
    services = await services_crud.get_multi(session=session)
    keyboard = InlineKeyboardBuilder()
    for service in services:
        if service.category_id == category.id:
            keyboard.row(InlineKeyboardButton(text=f'{service.name}',
                                              callback_data=f'categories_from_BU_{service.id}'))
    await callback.message.answer(
        text='Выберите услугу',
        reply_markup=keyboard.as_markup()
    )
    await callback.message.delete()


@router.callback_query(F.data.startswith('categories_from_BU_'))
async def get_all_services_business_unit(
    callback: CallbackQuery,
    session: AsyncSession
):
    service_bu = await business_units_crud.get(
        obj_id=int(callback.data.split('_')[-1]), session=session
    )
    services = await services_crud.get_multi(session=session)
    keyboard = InlineKeyboardBuilder()
    for service_bu in services:
        if service_bu.business_units_id == service_bu.id:
            keyboard.row(InlineKeyboardButton(text=f'{service_bu.name}',
                                              callback_data=f'categories_from_BU_{service_bu.id}'))
    await callback.message.answer(
        text='Можно заказать в:',
        reply_markup=keyboard.as_markup()
    )
    await callback.message.delete()
