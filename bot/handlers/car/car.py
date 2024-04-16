from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession
from bot.states.car_states import RegCar
from bot.keyboards.users_keyboards import back_menu_kb
from bot.keyboards.cars_keyboards import car_kb
from bot.db.crud.cars import cars_crud
from bot.db.crud.users import users_crud
from bot.core.constants import (PROFILE_MESSAGE_WITH_INLINE,)
router = Router(name=__name__)

car_message = (
    'Ваш автомобиль:\n'
    'Брэнд: {brand}\n'
    'Модел: {model}\n'
    'Номер: {number}\n'
)


@router.callback_query(F.data == 'view_car')
async def get_profile(
    callback: CallbackQuery,
    session: AsyncSession,
):

    await callback.message.delete()
    tg_id = callback.from_user.id
    user = await users_crud.get_by_attribute(attr_name='tg_user_id',
                                             attr_value=tg_id,
                                             session=session)
    db_obj = await cars_crud.get_by_attribute(attr_name='user_id',
                                              attr_value=user.id,
                                              session=session)
    await callback.message.answer(
        car_message.format(
            brand=db_obj.brand,
            model=db_obj.model,
            number=db_obj.number
        ),
        reply_markup=back_menu_kb
    )


@router.callback_query(F.data == 'car_menu')
async def main_user_menu(
    callback: CallbackQuery,
    session: AsyncSession,
):
    await callback.message.delete()
    await callback.message.answer(
        PROFILE_MESSAGE_WITH_INLINE,
        reply_markup=car_kb
    )


@router.message(F.data == 'add_car')
async def reg_car_brand(
    message: Message, state: FSMContext, session: AsyncSession
):
    await state.set_state(RegCar.brand)
    await message.answer('Введите брэнд автомобиля.')


@router.message(RegCar.brand)
async def reg_car_model(msg: Message,
                        state: FSMContext,
                        session: AsyncSession):
    await state.update_data(brand=msg.text)
    await state.set_state(RegCar.model)
    await msg.answer('Введите модель автомобиля.')


@router.message(RegCar.brand)
async def reg_car_number(msg: Message,
                         state: FSMContext,
                         session: AsyncSession):
    await state.update_data(model=msg.text)
    await state.set_state(RegCar.number)
    await msg.answer('Введите номер автомобиля.')


@router.message(RegCar.number)
async def reg_car_finish(msg: Message,
                         state: FSMContext,
                         session: AsyncSession):
    await state.update_data(number=msg.text)
    data = await state.get_data()
    await msg.answer('Спасибо за регистрацию!')
    await state.clear()
    await cars_crud.create(obj_in=data, session=session)
    await msg.answer(
        f'Вы зарегестрировали автомобиль такими данными:\n'
        f'Брэнд: {data["brand"]}\n'
        f'Модель: {data["model"]}\n'
        f'Номер: {data["number"]}'
    )
    return data
