from aiogram import F, Router
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup)
from sqlalchemy.ext.asyncio import AsyncSession
from bot.db.crud.services import services_crud
from bot.db.crud.categories import category_crud
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.keyboards.categories_keyboard import service_category_kb

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
    await callback.message.delete()
    await callback.message.answer(
        text='Выберите категорию',
        reply_markup=keyboard.as_markup()
    )


@router.callback_query(F.data.startswith('categories_from_service_'))
async def get_all_services(
    callback: CallbackQuery,
    session: AsyncSession
):
    category = await category_crud.get(
        obj_id=int(callback.data.split('_')[-1]), session=session
    )
    await callback.message.delete()
    services = await services_crud.get_multi(session=session)
    for service in services:
        if service.category_id == category.id:
            await callback.message.answer(
                text=f'{category.name} {service.name} {service.note}',
                reply_markup=service_category_kb(service)
            )
            return


@router.callback_query(F.data.startswith('services_from_BU_'))
async def get_all_services_business_unit(
    callback: CallbackQuery,
    session: AsyncSession
):
    service = await services_crud.get(
        obj_id=int(callback.data.split('_')[-1]), session=session
    )
    await callback.message.delete()
    msg = f'Услугу {service.name} можно заказать в:'
    for bu in service.business_units:
        msg += f'{bu.name} {bu.note} {bu.address}'
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
        text='Вернуться к списку услуг',
        callback_data='service_catalog'
        )
        ]])
    
    await callback.message.answer(
        text=msg,
        reply_markup=keyboard
    )
