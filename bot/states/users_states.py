
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram import Router, F
from core.validators import user_check_before_reg

router = Router(name=__name__)

class RegUser(StatesGroup):
    fio = State()
    
    birth_date = State()
    phone_number = State()
    tg_user_id = State()


@router.message(F.text =='Регистрация') 
async def testing_user(message: Message, state: FSMContext, session: AsyncSession):
    user_id = message.from_user.id
    if await user_check_before_reg(tg_user_id=user_id,session=session):
        await state.set_state(RegUser.fio)
        await message.answer('Введите ФИО в формате Иванов Иван Иванович')


@router.message(RegUser.fio)
async def reg_fio(msg: Message, state:FSMContext):
    await state.update_data(fio=msg.text)
    await state.set_state(RegUser.birth_date)
    await msg.answer('Введите дату рождения в формате 01.02.3000')


@router.message(RegUser.birth_date)
async def reg_birth_date(msg: Message, state:FSMContext):
    await state.update_data(birth_date=msg.text)
    await state.set_state(RegUser.phone_number)
    await msg.answer('Введите контакт')


@router.message(RegUser.phone_number)
async def reg_birth_date(msg: Message, state:FSMContext):
    await state.update_data(phone_number=msg.text)
    data = await state.get_data()
    await msg.answer('Спасибо за регистрацию!')
    await state.clear()
    data['tg_user_id'] = msg.from_user.id
    print(data)
    return data
    