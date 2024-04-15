from aiogram import F, Router
from aiogram.types import CallbackQuery, InlineKeyboardButton
from sqlalchemy.ext.asyncio import AsyncSession
from bot.db.crud.services import category_crud, services_crud
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router(name=__name__)


@router.callback_query(F.data == 'service_catalog')
async def get_all_category(callback: CallbackQuery, session: AsyncSession):
    categories = await category_crud.get_multi(session=session)
    keyboard = InlineKeyboardBuilder()
    for i, category in enumerate(categories):
        keyboard.row(InlineKeyboardButton(text=f'{category.name}',
                                          callback_data=f'{category.id}'))
    await callback.message.answer(
        text='Выберите категорию',
        reply_markup=keyboard.as_markup()
    )

    category_id = callback.data

    service = await services_crud.get(session=session, obj_id=category_id)

    if service is not None:
        await callback.message.answer(
            text=f'Вы выбрали категорию {category.name}.\n\nСоответствующая услуга: {service.name}.',
            reply_markup=keyboard.as_markup()
            )
    else:
        await callback.message.answer(
            text='Ошибка при получении услуги.',
            reply_markup=None
        )
