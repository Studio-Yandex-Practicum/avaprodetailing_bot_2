from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.crud.users_crud import user_crud
from bot.keyboards.users_keyboards import agree_refuse_kb
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
        'Введите ФИО в формате Иванов Иван Иванович'
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
        await msg.answer('Введите дату рождения в формате 01.02.3000')
    else:
        await msg.answer('Введите ФИО в формате Иванов Иван Иванович')
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
        await msg.answer('Введите номер телефона в формате +78888888888')
    else:
        await msg.answer('Введите дату рождения в формате 01.02.3000')
    await msg.delete()


@router.message(RegUser.phone_number)
async def reg_birth_date(
    msg: Message,
    state: FSMContext,
    session: AsyncSession
):
    #await msg.delete()
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
        await msg.answer('Введите номер телефона в формате +78888888888')


@router.callback_query(F.data == 'agree')
async def registrate_agree(
    callback: CallbackQuery,

    state: FSMContext,
    session: AsyncSession,
):
    await callback.message.delete()
    data = await state.get_data()
    await callback.message.answer('Спасибо за регистрацию!')
    await state.clear()
    data['tg_user_id'] = callback.from_user.id
    await user_crud.create(obj_in=data, session=session)
    await callback.message.answer('Теперь Вам доступны все функции бота')
