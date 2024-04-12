from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession
#from bot.db.crud.users_crud import user_crud
from bot.core.constants import (STATE_BIRTH_DATE, STATE_FIO,
                                STATE_PHONE_NUMBER, THX_REG)
from bot.db.crud.users import users_crud
from bot.db.models.users import User
from bot.keyboards.users_keyboards import add_car_kb, agree_refuse_kb
from bot.states.user_states import RegUser
from bot.utils.validators import (validate_birth_date, validate_fio,
                                  validate_phone_number)

router = Router(name=__name__)



reg_message = (
    'Вы зарегестрировались с такими данными:\n'
    'ФИО: {fio}\n'
    'Дата рождения: {birth_date}\n'
    'Номер телефона: {phone_number}\n'
    '\n'
    'Нажимая на "Согласиться" Вы подтверждаете корректность и даете '
    'согласие на использование данных.'
)


@router.callback_query(F.data == 'Registration')
async def testing_user(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
):
    await state.clear()
    await callback.message.delete()

    await state.set_state(RegUser.fio)
    await callback.message.answer(
        STATE_FIO
    )
    await callback.answer()


@router.message(RegUser.fio)
async def reg_fio(msg: Message, state: FSMContext):
    await msg.bot.delete_message(
        chat_id=msg.from_user.id,
        message_id=msg.message_id - 1
    )
    if not await validate_fio(msg=msg.text):
        await msg.answer(STATE_FIO)
        return
    await state.update_data(fio=msg.text)
    await state.set_state(RegUser.birth_date)
    await msg.answer(STATE_BIRTH_DATE)
    await msg.delete()


@router.message(RegUser.birth_date)
async def reg_birth_date(msg: Message, state: FSMContext):
    await msg.bot.delete_message(
        chat_id=msg.from_user.id,
        message_id=msg.message_id - 1
    )
    if not await validate_birth_date(msg=msg.text):
        await msg.answer(STATE_BIRTH_DATE)
        return
    await state.update_data(birth_date=msg.text)
    await state.set_state(RegUser.phone_number)
    await msg.answer(STATE_PHONE_NUMBER)
    await msg.delete()


@router.message(RegUser.phone_number)
async def reg_phone_number(
    msg: Message,
    state: FSMContext,
    session: AsyncSession
):
    await msg.bot.delete_message(
        chat_id=msg.from_user.id,
        message_id=msg.message_id - 1
    )
    if not await validate_phone_number(msg=msg.text):
        await msg.answer(STATE_PHONE_NUMBER)
        return
    await state.update_data(phone_number=msg.text)
    data = await state.get_data()
    await msg.answer(
        reg_message.format(
            fio=data["fio"], 
            birth_date=data["birth_date"], 
            phone_number=data["phone_number"]
        ),
        reply_markup=agree_refuse_kb
    )
    await msg.delete()


@router.callback_query(F.data == 'agree')
async def registrate_agree(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
):

    await callback.message.delete()
    data = await state.get_data()
    await state.clear()
    data['tg_user_id'] = callback.from_user.id
    await users_crud.create(obj_in=data, session=session)
    await callback.message.answer(
        THX_REG,
        reply_markup=add_car_kb
    )
