from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.crud.cars import cars_crud
from bot.db.crud.users import users_crud
from bot.keyboards.cars_keyboards import (
    add_car_kb, car_kb, edit_car_kb,
    finish_add_car_kb,
    verify_delete_car_kb,
)
from bot.states.car_states import ChooseCar, RegCar
from bot.utils.validators import verify_symbols
from bot.core.enums import CarBodyType

router = Router(name=__name__)


@router.callback_query(F.data == 'car_menu')
async def car_menu(
    callback: CallbackQuery,
    session: AsyncSession,
):

    await callback.message.delete()
    tg_id = callback.from_user.id
    user = await users_crud.get_by_attribute(
        attr_name='tg_user_id',
        attr_value=tg_id,
        session=session
    )
    cars = user.cars
    if not cars:
        await callback.message.answer(
            "Внесите информацию по автомобилю",
            reply_markup=add_car_kb
        )
    else:
        car_message = 'Список авто: \n'
        for car in list(cars):
            car_message += (
                f"{car.brand} {car.model} | {car.number}\n"
            )

        await callback.message.answer(
            car_message,
            reply_markup=car_kb
        )


@router.callback_query(F.data == 'choose_car')
async def choose_car(
    callback: CallbackQuery,
    session: AsyncSession,
):

    await callback.message.delete()
    tg_id = callback.from_user.id
    user = await users_crud.get_by_attribute(
        attr_name='tg_user_id',
        attr_value=tg_id,
        session=session
    )
    cars = user.cars
    car_message = 'Выберите автомобиль'
    choose_car_kb = InlineKeyboardBuilder()
    sizes = []
    for car in cars:
        car_name = f" Авто: {car.brand}/{car.model} - {car.number}"
        choose_car_kb.button(text=car_name, callback_data=f'car_{car.id}')
        sizes += [1]
    choose_car_kb.adjust(*sizes)
    await callback.message.answer(
        car_message,
        reply_markup=choose_car_kb.as_markup()
    )


@router.callback_query(F.data.startswith("car_"))
async def edit_car(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
):
    await callback.message.delete()
    car_id = int(callback.data.split('_')[1])
    car = await cars_crud.get(obj_id=car_id, session=session)
    await state.set_state(ChooseCar.chosen)
    await state.update_data(chosen=car)
    await callback.message.answer(
        (
            "Выберите действие для\n"
            f"{car.brand}/{car.model} - {car.number}"),
        reply_markup=edit_car_kb
    )


@router.callback_query(F.data == 'delete_car')
async def car_delete_verify(
    callback: CallbackQuery, state: FSMContext,
    session: AsyncSession
):
    await callback.message.delete()
    await callback.message.answer(
        'Вы действительно хотите удалить автомобиль из списка?',
        reply_markup=verify_delete_car_kb
    )


@router.callback_query(F.data == 'confirmed_delete')
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
        reply_markup=car_kb
    )


@router.callback_query(F.data == 'change_number')
async def car_change_number(
    callback: CallbackQuery, state: FSMContext,
    session: AsyncSession
):
    await callback.message.delete()

    await state.set_state(ChooseCar.new_number)
    msg = await callback.message.answer(
        'Введите гос. номер автомобиля.'
    )
    await state.update_data(
        msg_id=msg.message_id
    )
    await callback.answer()


@router.message(ChooseCar.new_number)
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
            reply_markup=edit_car_kb
        )
        await msg.delete()


@router.callback_query(F.data == 'change_brand')
async def car_change_brand(
    callback: CallbackQuery, state: FSMContext,
    session: AsyncSession
):
    await callback.message.delete()

    await state.set_state(ChooseCar.new_brand)
    msg = await callback.message.answer(
        'Введите брэнд автомобиля.'
    )
    await state.update_data(
        msg_id=msg.message_id
    )
    await callback.answer()


@router.message(ChooseCar.new_brand)
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
            reply_markup=edit_car_kb
        )
        await msg.delete()


@router.callback_query(F.data == 'change_bodytype')
async def car_change_bodytype(
    callback: CallbackQuery, state: FSMContext,
    session: AsyncSession, msg: Message,
):
    await callback.message.delete()
    state_data = await state.get_data()
    await state.set_state(RegCar.bodytype)
    choose_car_kb = InlineKeyboardBuilder()
    sizes = []
    for body in CarBodyType:
        body_name = f" {body.value}"
        choose_car_kb.button(text=body_name,
                             callback_data=f'edit_body_{body.name}')
        sizes += [1]
    choose_car_kb.adjust(*sizes)
    await msg.bot.edit_message_text(
        chat_id=msg.from_user.id,
        message_id=state_data['msg_id'],
        text='Выберите кузов автомобиля.',
        reply_markup=choose_car_kb
    )
    await msg.delete()


@router.callback_query(F.data.startswith("edit_body_"))
async def car_change_bodytype_confirm(
    msg: Message,
    state: FSMContext,
    session: AsyncSession,
    callback: CallbackQuery,
):
    state_data = await state.get_data()
    await callback.message.delete()
    body = CarBodyType[callback.data.split('_')[2]]
    await state.update_data(bodytype=body)

    await cars_crud.update(
            state_data['chosen'],
            {"bodytype": body},
            session=session, )
    await msg.bot.edit_message_text(
            chat_id=msg.from_user.id,
            message_id=state_data['msg_id'],
            text='Тип кузова изменён',
            reply_markup=edit_car_kb
        )
    await msg.delete()


@router.callback_query(F.data == 'change_model')
async def car_change_model(
    callback: CallbackQuery, state: FSMContext,
    session: AsyncSession
):
    await callback.message.delete()

    await state.set_state(ChooseCar.new_model)
    msg = await callback.message.answer(
        'Введите модель автомобиля.'
    )
    await state.update_data(
        msg_id=msg.message_id
    )
    await callback.answer()


@router.message(ChooseCar.new_model)
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
            reply_markup=edit_car_kb
        )
        await msg.delete()


@router.callback_query(F.data == 'add_car')
async def reg_car_start(
    callback: CallbackQuery, state: FSMContext,
    session: AsyncSession
):
    await state.clear()
    await callback.message.delete()
    tg_id = callback.from_user.id
    user = await users_crud.get_by_attribute(
        attr_name='tg_user_id',
        attr_value=tg_id,
        session=session
    )
    await state.update_data(user_id=user.id)

    await state.set_state(RegCar.brand)
    msg = await callback.message.answer(
        'Введите брэнд автомобиля.'
    )
    await state.update_data(
        msg_id=msg.message_id
    )
    await callback.answer()


@router.message(RegCar.brand)
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
    await state.set_state(RegCar.model)
    await msg.delete()


@router.message(RegCar.model)
async def reg_car_model(
    msg: Message,
    state: FSMContext,
    session: AsyncSession
):
    state_data = await state.get_data()

    await state.update_data(model=msg.text)
    await state.set_state(RegCar.bodytype)

    choose_car_kb = InlineKeyboardBuilder()
    sizes = []
    for body in CarBodyType:
        car_name = f" Авто: {body.value}"
        choose_car_kb.button(text=car_name, callback_data=f'body_{body.name}')
        sizes += [1]
    choose_car_kb.adjust(*sizes)

    await msg.bot.edit_message_text(
        chat_id=msg.from_user.id,
        message_id=state_data['msg_id'],
        text='Выберите кузов автомобиля.',
        reply_markup=choose_car_kb
    )
    await msg.delete()


@router.callback_query(F.data.startswith("body_"))
async def reg_car_bodytype(
    msg: Message,
    state: FSMContext,
    session: AsyncSession,
    callback: CallbackQuery,
):
    state_data = await state.get_data()
    await callback.message.delete()
    body = CarBodyType[callback.data.split('_')[1]]
    await state.update_data(bodytype=body)
    await state.set_state(RegCar.number)

    await msg.bot.edit_message_text(
        chat_id=msg.from_user.id,
        message_id=state_data['msg_id'],
        text='Введите номер автомобиля.'
    )
    await msg.delete()


@router.message(RegCar.number)
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
              f'Тип кузова: {data["bodytype"]}'
              f'Номер: {data["number"]}'),
        reply_markup=finish_add_car_kb
    )

    return data
