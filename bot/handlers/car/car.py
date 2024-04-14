from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.states.car_states import RegCar

router = Router(name=__name__)


@router.message(F.text == 'Регистрация автомобиля')
async def reg_car_brand(
    message: Message, state: FSMContext, session: AsyncSession
):
    await state.set_state(RegCar.brand)
    await message.answer('Введите брэнд автомобиля.')


@router.message(RegCar.brand)
async def reg_car_model(msg: Message, state: FSMContext):
    await state.update_data(brand=msg.text)
    await state.set_state(RegCar.model)
    await msg.answer('Введите модель автомобиля.')


@router.message(RegCar.brand)
async def reg_car_number(msg: Message, state: FSMContext):
    await state.update_data(model=msg.text)
    await state.set_state(RegCar.number)
    await msg.answer('Введите номер автомобиля.')


@router.message(RegCar.number)
async def reg_car_finish(msg: Message, state: FSMContext):
    await state.update_data(number=msg.text)
    data = await state.get_data()
    await msg.answer('Спасибо за регистрацию!')
    await state.clear()
    data['tg_user_id'] = msg.from_user.id
    await msg.answer(
        f'Вы зарегестрировали автомобиль такими данными:\n'
        f'Брэнд: {data["brand"]}\n'
        f'Модель: {data["model"]}\n'
        f'Номер: {data["number"]}'
    )
    return data
