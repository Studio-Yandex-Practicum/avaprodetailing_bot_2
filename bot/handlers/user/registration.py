from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

# from bot.db.crud.users_crud import user_crud
from bot.core.constants import (STATE_BIRTH_DATE, STATE_FIO,
                                STATE_PHONE_NUMBER, THX_REG)
from bot.db.crud.users import users_crud
from bot.db.models.users import User
# from bot.handlers.admin.bonus_management import award_registration_bonus
from bot.keyboards.users_keyboards import add_car_kb, agree_refuse_kb
from bot.states.user_states import RegUser
from bot.utils.validators import (validate_birth_date, validate_fio,
                                  validate_phone_number)

router = Router(name=__name__)

reg_message = (
    'Вы зарегистрировались с такими данными:\n'
    'ФИО: {fio}\n'
    'Дата рождения: {birth_date}\n'
    'Номер телефона: {phone_number}\n'
    '\n'
    'Нажимая на "Согласиться" Вы подтверждаете корректность и даете '
    'согласие на использование данных.'
)
error_message = (
    'Неверный формат ввода\n'
    '{info_text}\n'
    'Вы ввели {incorrect}'
)


@router.callback_query(F.data == 'Registration')
async def testing_user(
    callback: CallbackQuery,
    state: FSMContext,
):
    await state.clear()
    await callback.message.delete()

    await state.set_state(RegUser.fio)
    msg = await callback.message.answer(
        STATE_FIO
    )
    await state.update_data(
        msg_id=msg.message_id
    )
    await callback.answer()


@router.message(RegUser.fio)
async def reg_fio(msg: Message, state: FSMContext):
    state_data = await state.get_data()

    if not await validate_fio(msg=msg.text):
        await msg.delete()
        await msg.bot.edit_message_text(
            chat_id=msg.from_user.id,
            message_id=state_data['msg_id'],
            text=error_message.format(
                info_text=STATE_FIO,
                incorrect=msg.text
            )
        )
        return
    await msg.bot.edit_message_text(
        chat_id=msg.from_user.id,
        message_id=state_data['msg_id'],
        text=STATE_BIRTH_DATE
    )
    await state.update_data(fio=msg.text)
    await state.set_state(RegUser.birth_date)
    await msg.delete()


@router.message(RegUser.birth_date)
async def reg_birth_date(msg: Message, state: FSMContext):
    state_data = await state.get_data()
    if not await validate_birth_date(msg=msg.text):
        await msg.delete()
        await msg.bot.edit_message_text(
            chat_id=msg.from_user.id,
            message_id=state_data['msg_id'],
            text=error_message.format(
                info_text=STATE_BIRTH_DATE,
                incorrect=msg.text
            )
        )
        return
    await state.update_data(birth_date=msg.text)
    await state.set_state(RegUser.phone_number)

    await msg.bot.edit_message_text(
        chat_id=msg.from_user.id,
        message_id=state_data['msg_id'],
        text=STATE_PHONE_NUMBER
    )
    await msg.delete()


@router.message(RegUser.phone_number)
async def reg_phone_number(
    msg: Message,
    state: FSMContext,
    session: AsyncSession
):
    state_data = await state.get_data()
    if not await validate_phone_number(phone_number=msg.text):
        await msg.delete()
        await msg.bot.edit_message_text(
            chat_id=msg.from_user.id,
            message_id=state_data['msg_id'],
            text=error_message.format(
                info_text=STATE_PHONE_NUMBER,
                incorrect=msg.text
            )
        )
        return
    await state.update_data(phone_number=msg.text)
    data = await state.get_data()
    await msg.bot.edit_message_text(
        text=reg_message.format(
            fio=data["fio"],
            birth_date=data["birth_date"],
            phone_number=data["phone_number"]
        ),
        chat_id=msg.from_user.id,
        message_id=state_data['msg_id'],
        reply_markup=agree_refuse_kb
    )
    await msg.delete()


@router.callback_query(F.data == 'agree')
async def registrate_agree(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
):
    data = await state.get_data()
    await state.clear()
    data['tg_user_id'] = callback.from_user.id
    new_user = await users_crud.create(obj_in=data, session=session)
    # TODO
    # user11 = await users_crud.get_by_attribute(
    #    session=session,
    #    attr_name='phone_number',
    #    attr_value=data['phone_number'],
    # )
    # await award_registration_bonus(new_user, session)
    await callback.bot.edit_message_text(
        THX_REG,
        chat_id=callback.from_user.id,
        message_id=data['msg_id'],
        reply_markup=add_car_kb,
    )
