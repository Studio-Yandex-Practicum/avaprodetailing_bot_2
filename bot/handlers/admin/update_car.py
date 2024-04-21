from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.crud.cars import cars_crud
from bot.db.crud.users import users_crud
from bot.keyboards.admin_keyboards import (
    admin_car_kb, admin_edit_car_kb,
    finish_add_car_kb,
    admin_verify_delete_car_kb,
)
from bot.states.user_states import AdminState
from bot.utils.validators import verify_symbols

router = Router(name=__name__)


@router.callback_query(F.data == 'update_car_data')
async def admin_choose_car(
    callback: CallbackQuery,
    session: AsyncSession,
    state: FSMContext,
):

    await callback.message.delete()
    state_data = await state.get_data()
    user = await users_crud.get_by_attribute(
        attr_name='phone_number',
        attr_value=state_data['phone_number'],
        session=session
    )
    cars = user.cars
    car_message = 'Выберите автомобиль клиента'
    choose_car_kb = InlineKeyboardBuilder()
    choose_car_kb.button(text="Добавить автомобиль",
                         callback_data="admin_add_car")
    sizes = [1]
    for car in cars:
        car_name = f" Авто: {car.brand}/{car.model} - {car.number}"
        choose_car_kb.button(text=car_name, callback_data=f'admincar_{car.id}')
        sizes += [1]
    choose_car_kb.adjust(*sizes)
    await callback.message.answer(
        car_message,
        reply_markup=choose_car_kb.as_markup()
    )


@router.callback_query(F.data.startswith("admincar_"))
async def edit_car(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
):
    await callback.message.delete()
    car_id = int(callback.data.split('_')[1])
    car = await cars_crud.get(obj_id=car_id, session=session)
    await state.set_state(AdminState.chosen_car)
    await state.update_data(chosen=car)
    await callback.message.answer(
        (
            "Выберите действие для\n"
            f"{car.brand}/{car.model} - {car.number}"),
        reply_markup=admin_edit_car_kb
    )


@router.callback_query(F.data == 'admin_delete_car')
async def car_delete_verify(
    callback: CallbackQuery, state: FSMContext,
    session: AsyncSession
):
    await callback.message.delete()
    await callback.message.answer(
        'Вы действительно хотите удалить автомобиль из списка?',
        reply_markup=admin_verify_delete_car_kb
    )


@router.callback_query(F.data == 'admin_confirmed_delete')
async def car_delete(
    callback: CallbackQuery, state: FSMContext,
    session: AsyncSession
):
    await callback.message.delete()
    state_data = await state.get_data()
    await cars_crud.remove(session=session, db_obj=state_data['chosen'])
    await state.clear()
    await callback.message.answer(
        'Автомобиль удалён',
        reply_markup=admin_car_kb
    )


@router.callback_query(F.data == 'admin_change_number')
async def car_change_number(
    callback: CallbackQuery, state: FSMContext,
    session: AsyncSession
):
    await callback.message.delete()

    await state.set_state(AdminState.number_update)
    msg = await callback.message.answer(
        'Введите гос. номер автомобиля.'
    )
    await state.update_data(
        msg_id=msg.message_id
    )
    await callback.answer()


@router.message(AdminState.number_update)
async def car_change_number_verify(
    msg: Message,
    state: FSMContext,
    session: AsyncSession
):
    state_data = await state.get_data()
    if not verify_symbols(msg.text):
        await msg.bot.edit_message_text(
            chat_id=msg.from_user.id,
            message_id=state_data['msg_id'],
            text='Не используйте спец. символы'
        )
        await msg.delete()
        return
    else:
        await state.update_data(new_number=msg.text)
        await cars_crud.update(
            state_data['chosen'],
            {"number": msg.text},
            session=session, )
        await msg.bot.edit_message_text(
            chat_id=msg.from_user.id,
            message_id=state_data['msg_id'],
            text='Номер автомобиля изменён',
            reply_markup=admin_edit_car_kb
        )
        await msg.delete()


@router.callback_query(F.data == 'admin_change_brand')
async def car_change_brand(
    callback: CallbackQuery, state: FSMContext,
    session: AsyncSession
):
    await callback.message.delete()

    await state.set_state(AdminState.brand_update)
    msg = await callback.message.answer(
        'Введите брэнд автомобиля.'
    )
    await state.update_data(
        msg_id=msg.message_id
    )
    await callback.answer()


@router.message(AdminState.brand_update)
async def car_change_brand_verify(
    msg: Message,
    state: FSMContext,
    session: AsyncSession
):
    state_data = await state.get_data()
    if not verify_symbols(msg.text):
        await msg.bot.edit_message_text(
            chat_id=msg.from_user.id,
            message_id=state_data['msg_id'],
            text='Не используйте спец. символы'
        )
        await msg.delete()
        return
    else:
        await state.update_data(new_number=msg.text)
        await cars_crud.update(
            state_data['chosen'],
            {"brand": msg.text},
            session=session, )
        await msg.bot.edit_message_text(
            chat_id=msg.from_user.id,
            message_id=state_data['msg_id'],
            text='Брэнд автомобиля изменён',
            reply_markup=admin_edit_car_kb
        )
        await msg.delete()


@router.callback_query(F.data == 'admin_change_model')
async def car_change_model(
    callback: CallbackQuery, state: FSMContext,
    session: AsyncSession
):
    await callback.message.delete()

    await state.set_state(AdminState.model_update)
    msg = await callback.message.answer(
        'Введите модель автомобиля.'
    )
    await state.update_data(
        msg_id=msg.message_id
    )
    await callback.answer()


@router.message(AdminState.model_update)
async def car_change_model_verify(
    msg: Message,
    state: FSMContext,
    session: AsyncSession
):
    state_data = await state.get_data()
    if not verify_symbols(msg.text):
        await msg.bot.edit_message_text(
            chat_id=msg.from_user.id,
            message_id=state_data['msg_id'],
            text='Не используйте спец. символы'
        )
        await msg.delete()
        return
    else:
        await state.update_data(new_number=msg.text)
        await cars_crud.update(
            state_data['chosen'],
            {"model": msg.text},
            session=session, )
        await msg.bot.edit_message_text(
            chat_id=msg.from_user.id,
            message_id=state_data['msg_id'],
            text='Модель автомобиля изменена',
            reply_markup=admin_edit_car_kb
        )
        await msg.delete()


@router.callback_query(F.data == 'admin_add_car')
async def reg_car_start(
    callback: CallbackQuery, state: FSMContext,
    session: AsyncSession
):
    await callback.message.delete()
    state_data = await state.get_data()
    user = await users_crud.get_by_attribute(
        attr_name='phone_number',
        attr_value=state_data['phone_number'],
        session=session
    )
    await state.update_data(user_id=user.id)

    await state.set_state(AdminState.brand)
    msg = await callback.message.answer(
        'Введите брэнд автомобиля.'
    )
    await state.update_data(
        msg_id=msg.message_id
    )
    await callback.answer()


@router.message(AdminState.brand)
async def reg_car_brand(
    msg: Message,
    state: FSMContext,
    session: AsyncSession
):
    state_data = await state.get_data()
    await msg.bot.edit_message_text(
        chat_id=msg.from_user.id,
        message_id=state_data['msg_id'],
        text='Введите модель автомобиля.'
    )
    await state.update_data(brand=msg.text)
    await state.set_state(AdminState.model)
    await msg.delete()


@router.message(AdminState.model)
async def reg_car_model(
    msg: Message,
    state: FSMContext,
    session: AsyncSession
):
    state_data = await state.get_data()

    await state.update_data(model=msg.text)
    await state.set_state(AdminState.number)

    await msg.bot.edit_message_text(
        chat_id=msg.from_user.id,
        message_id=state_data['msg_id'],
        text='Введите номер автомобиля.'
    )
    await msg.delete()


@router.message(AdminState.number)
async def reg_car_number(
    msg: Message,
    state: FSMContext,
    session: AsyncSession
):
    await state.update_data(number=msg.text)
    data = await state.get_data()
    await state.clear()
    await cars_crud.create(obj_in=data, session=session)
    await msg.delete()
    await msg.bot.edit_message_text(
        chat_id=msg.from_user.id,
        message_id=data['msg_id'],
        text=(f'Вы зарегистрировали автомобиль такими данными:\n'
              f'Брэнд: {data["brand"]}\n'
              f'Модель: {data["model"]}\n'
              f'Номер: {data["number"]}'),
        reply_markup=finish_add_car_kb
    )

    return data


# FIXME car_body_type забыл
