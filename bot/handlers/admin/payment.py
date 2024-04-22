from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.crud.cars import cars_crud
from bot.db.crud.services import services_crud
from bot.db.crud.users import users_crud
from bot.db.crud.visit_crud import visit_crud
from bot.keyboards.bonus_keyboards import bonus_admin
from bot.keyboards.payment_inline import (build_services_keyboard,
                                          build_user_cars_keyboard)
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
    await state.update_data(user_id=user.id)
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
    car = await cars_crud.get(
        obj_id=int(callback_query.data.split('_')[-1]), session=session
    )
    await state.update_data(car=car)
    admin = await users_crud.get_by_attribute(
        attr_name='tg_user_id',
        attr_value=callback_query.from_user.id,
        session=session
    )
    await state.update_data(admin_user_id=admin.id)
    business_unit = admin.business_unit
    if business_unit is None:
        await callback_query.message.bot.edit_message_text(
            message_id=state_data['msg_id'],
            chat_id=callback_query.from_user.id,
            text='Не найден бизнес-юнит у администратора.'
        )
        return
    services = admin.business_unit.services
    await state.update_data(chosen_services=[])
    await state.update_data(business_unit_id=business_unit.id)
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
    visit_info = 'Введите общую сумму посещения:'
    state_data = await state.get_data()
    await callback_query.message.bot.edit_message_text(
        text=visit_info,
        chat_id=callback_query.from_user.id,
        message_id=state_data['msg_id']
    )
    await state.set_state(AdminState.payment_amount)


@router.message(AdminState.payment_amount)
async def manage_bonus_callback(
    message: types.Message, state: FSMContext, session: AsyncSession
):
    if not message.text.isdigit() and int(message.text) >= 0:
        await message.answer('Введите корректную положительную сумму.')
        return
    payment_amount = int(message.text)
    await state.update_data(payment_amount=int(message.text))
    state_data = await state.get_data()
    user = await users_crud.get_by_attribute(
        attr_name='phone_number',
        attr_value=state_data['phone_number'],
        session=session
    )
    services = []
    for service_id in state_data['chosen_services']:
        service = await services_crud.get(
            obj_id=service_id, session=session
        )
        services.append(service.name)
    service_names = ', '.join(services)
    await state.update_data(chosen_services=service_names)
    await state.update_data(
        bonus_to_spend=min(user.balance, int(payment_amount * 0.98))
    )
    state_data = await state.get_data()
    await visit_crud.create(
        obj_in=state_data,
        session=session
    )
    await message.bot.edit_message_text(
        f"Посещение клиента:\n"
        f"Автомобиль {state_data['car'].brand} {state_data['car'].number}\n"
        f"Услуги: {service_names}\n"
        f"К оплате {payment_amount} рублей\n\n"
        f"У клиента {user.balance} баллов.\n"
        f" Может быть списано {state_data['bonus_to_spend']} баллов.",
        chat_id=message.from_user.id,
        message_id=state_data['msg_id'],
        reply_markup=bonus_admin
    )
    await message.delete()
