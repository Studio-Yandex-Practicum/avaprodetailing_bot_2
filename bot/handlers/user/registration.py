from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.core.constants import (STATE_BIRTH_DATE, STATE_FIO,
                                STATE_PHONE_NUMBER, THX_REG)
from bot.db.models.users import User
from bot.keyboards.users_keyboards import add_car_kb, agree_refuse_kb
from bot.states.user_states import RegUser
from bot.utils.validators import (validate_reg_birth_date, validate_reg_fio,
                                  validate_reg_phone_number)

router = Router(name=__name__)


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
    if await validate_reg_fio(msg=msg.text):
        await state.update_data(fio=msg.text)
        await state.set_state(RegUser.birth_date)
        await msg.answer(STATE_BIRTH_DATE)
    else:
        await msg.answer(STATE_FIO)
    await msg.delete()


@router.message(RegUser.birth_date)
async def reg_birth_date(msg: Message, state: FSMContext):
    await msg.bot.delete_message(
        chat_id=msg.from_user.id,
        message_id=msg.message_id - 1
    )
    if await validate_reg_birth_date(msg=msg.text):
        await state.update_data(birth_date=msg.text)
        await state.set_state(RegUser.phone_number)
        await msg.answer(STATE_PHONE_NUMBER)
    else:
        await msg.answer(STATE_BIRTH_DATE)
    await msg.delete()


@router.message(RegUser.phone_number)
async def reg_birth_date(
    msg: Message,
    state: FSMContext,
    session: AsyncSession
):
    await msg.bot.delete_message(
        chat_id=msg.from_user.id,
        message_id=msg.message_id - 1
    )
    if await validate_reg_phone_number(msg=msg.text):
        await state.update_data(phone_number=msg.text)
        data = await state.get_data()
        await msg.answer(
            f'Вы зарегестрировались с такими данными:\n'
            f'ФИО: {data["fio"]}\n'
            f'Дата рождения: {data["birth_date"]}\n'
            f'Номер телефона: {data["phone_number"]}\n'
            'Нажимая на "Согласиться" Вы подтверждаете корректность и даете '
            'согласие на использование данных.',
            reply_markup=agree_refuse_kb
        )
    else:
        await msg.answer(STATE_PHONE_NUMBER)
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
    await User.create(obj_in=data, session=session)
    await callback.message.answer(
        THX_REG,
        reply_markup=add_car_kb
    )
