from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.states.user_states import RegUser

router = Router(name=__name__)


@router.message(F.text == 'Регистрация')
async def testing_user(
    message: Message, state: FSMContext, session: AsyncSession
):
    await state.set_state(RegUser.fio)
    await message.answer('Введите ФИО в формате Иванов Иван Иванович')


@router.message(RegUser.fio)
async def reg_fio(msg: Message, state: FSMContext):
    await state.update_data(fio=msg.text)
    await state.set_state(RegUser.birth_date)
    await msg.answer('Введите дату рождения в формате 01.02.3000')


@router.message(RegUser.birth_date)
async def reg_birth_date(msg: Message, state: FSMContext):
    await state.update_data(birth_date=msg.text)
    await state.set_state(RegUser.phone_number)
    await msg.answer('Введите номер телефона')


@router.message(RegUser.phone_number)
async def reg_birth_date(msg: Message, state: FSMContext):
    await state.update_data(phone_number=msg.text)
    data = await state.get_data()
    await msg.answer('Спасибо за регистрацию!')
    await state.clear()
    data['tg_user_id'] = msg.from_user.id
    await msg.answer(
        f'Вы зарегестрировались с такими данными:\n'
        f'ФИО: {data["fio"]}\n'
        f'Дата рождения: {data["birth_date"]}\n'
        f'Номер телефона: {data["phone_number"]}'
    )
    return data
