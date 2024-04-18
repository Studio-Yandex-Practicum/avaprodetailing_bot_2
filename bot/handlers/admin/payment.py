from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.crud.business_units import business_units_crud
from bot.db.crud.car import cars_crud
from bot.db.crud.services import services_crud
from bot.db.crud.users import users_crud
from bot.keyboards.payment_inline import (
    build_services_keyboard,
    build_user_cars_keyboard,
)
from bot.states.user_states import AdminState

router = Router(name=__name__)


@router.callback_query(F.data == 'reg_visit')
async def register_visit_callback(
    callback_query: types.CallbackQuery,
    state: FSMContext,
    session: AsyncSession
):
    state_data = await state.get_data()
    user = await users_crud.get_by_attribute(
        attr_name='phone_number',
        attr_value=state_data['phone_number'],
        session=session
    )
    user_cars = user.cars
    if not user_cars:
        await callback_query.message.bot.edit_message_text(
            message_id=state_data['msg_id'],
            chat_id=callback_query.from_user.id,
            text=('У клиента не найдено ни одного автомобиля.'
                  '\nДобавьте его перед регистрацией посещения')
        )
        return
    keyboard = build_user_cars_keyboard(user.cars)
    await callback_query.message.bot.edit_message_text(
        message_id=state_data['msg_id'],
        chat_id=callback_query.from_user.id,
        text='Выберите автомобиль клиента:',
        reply_markup=keyboard
    )


@router.callback_query(F.data.startswith('car_selection_'))
async def select_services_callback(
    callback_query: types.CallbackQuery,
    state: FSMContext,
    session: AsyncSession
):
    state_data = await state.get_data()
    await state.update_data(car_id=int(callback_query.data.split('_')[-1]))
    # TODO: достаем услуги из точки, в которой работает админ по tg_user_id
    admin = await users_crud.get_by_attribute(
        attr_name='tg_user_id',
        attr_value=callback_query.from_user.id,
        session=session
    )
    services = admin.business_unit.services
    await state.update_data(chosen_services=[])
    await callback_query.message.bot.edit_message_text(
        message_id=state_data['msg_id'],
        chat_id=callback_query.from_user.id,
        text='Выберите оказанные услуги',
        reply_markup=build_services_keyboard(
            services, []
        )
    )


@router.callback_query(F.data.startswith('service_id_'))
async def service_choice_callback(
    callback_query: types.CallbackQuery,
    state: FSMContext,
    session: AsyncSession
):
    state_data = await state.get_data()
    chosen_services = state_data['chosen_services']
    selected_service = int(callback_query.data.split('_')[-1])
    if selected_service in chosen_services:
        chosen_services.remove(selected_service)
    else:
        chosen_services.append(selected_service)
    await state.update_data(chosen_services=chosen_services)
    admin = await users_crud.get_by_attribute(
        attr_name='tg_user_id',
        attr_value=callback_query.from_user.id,
        session=session
    )
    services = admin.business_unit.services
    await callback_query.message.bot.edit_message_reply_markup(
        message_id=state_data['msg_id'],
        chat_id=callback_query.from_user.id,
        reply_markup=build_services_keyboard(
            services, chosen_services
        )
    )


@router.callback_query(F.data == 'finish_selection')
async def finish_selection_callback(
    callback_query: types.CallbackQuery,
    state: FSMContext,
    session: AsyncSession
):
    await callback_query.message.delete()
    visit_info = 'Введите общую сумму посещения:'
    await callback_query.message.answer(
        visit_info,
    )
    await state.set_state(AdminState.payment_amount)


@router.message(AdminState.payment_amount)
async def payment_amount_callback(
    message: types.Message, state: FSMContext, session: AsyncSession
):
    try:
        payment_amount = int(message.text)
        if payment_amount <= 0:
            raise ValueError
    except ValueError:
        await message.answer('Введите корректную положительную сумму.')
        return
    await state.update_data(payment_amount=payment_amount)
