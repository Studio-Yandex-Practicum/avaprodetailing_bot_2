from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from bot.states.car_states import RegCar, ChooseCar
from bot.keyboards.users_keyboards import back_menu_kb
from bot.keyboards.info_keyboards import (
    info_kb, info_bonus_kb
)
from bot.db.crud.business_units import business_units_crud
from bot.db.crud.users import users_crud
from bot.utils.validators import verify_symbols
from bot.core.constants import (BONUS_DESCRIPTION,
                                SIGNUP_BONUS,
                                BONUS_LIFESPAN)

router = Router(name=__name__)


@router.callback_query(F.data == 'info')
async def info_menu(
    callback: CallbackQuery,
    session: AsyncSession,
):

    await callback.message.delete()
    await callback.message.answer(
        "Выберите раздел информации",
        reply_markup=info_kb
    )


@router.callback_query(F.data == 'info_business_unit')
async def choose_unit(
    callback: CallbackQuery,
    session: AsyncSession,
):

    await callback.message.delete()

    business_units = await business_units_crud.get_multi(session=session)
    admin = await users_crud.get_by_attribute(
        attr_name='tg_user_id',
        attr_value=callback.from_user.id,
        session=session
    )
    current_unit = admin.business_unit
    choose_unit_kb = InlineKeyboardBuilder()
    sizes = [1]
    for unit in business_units:
        choose_unit_kb.button(text=unit.name, callback_data=f'unit_{unit.id}')
        sizes += [1]
    choose_unit_kb.button(text="ОК", callback_data="info")
    choose_unit_kb.adjust(*sizes)
    services = ""
    for service in current_unit.services:
        services += f"{service.name}\n"
    await callback.message.answer(
        (f"{current_unit.name}\n"
         f"{current_unit.note}\n"
         f"{current_unit.address}"
         "Список услуг:\n"
         f"{services}"
         "Посмотреть информацию по другим бизнес-юнитам"),
        reply_markup=choose_unit_kb.as_markup()
    )


@router.callback_query(F.data.startswith("unit_"))
async def view_unit(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
):
    await callback.message.delete()
    unit_id = int(callback.data.split('_')[1])
    unit = await business_units_crud.get(obj_id=unit_id, session=session)
    services = ""
    for service in unit.services:
        services += f"{service.name}\n"
    await callback.message.answer(
        (f"{unit.name}\n"
         f"{unit.note}\n"
         f"{unit.address}"
         "Список услуг:\n"
         f"{services}"),
        reply_markup=info_bonus_kb
    )


@router.callback_query(F.data == 'info_bonus_programm')
async def view_bonus(
    callback: CallbackQuery,
    session: AsyncSession,
):

    await callback.message.delete()
    await callback.message.answer(
        BONUS_DESCRIPTION.format(
            signup_bonus=SIGNUP_BONUS,
            bonus_lifespan=BONUS_LIFESPAN),
        reply_markup=info_kb
    )
