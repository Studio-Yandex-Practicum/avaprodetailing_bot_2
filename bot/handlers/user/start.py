from aiogram import Router
from aiogram.filters import CommandStart, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.payload import decode_payload
from sqlalchemy.ext.asyncio import AsyncSession

from bot.core.constants import (
    PROFILE_MESSAGE_WITH_INLINE,
    WELCOME_ADMIN_MESSAGE, WELCOME_MESSAGE,
    WELCOME_REG_MESSAGE, CLIENT_BIO,
)
from bot.core.test_base import test_base
from bot.db.crud.users import users_crud
from bot.keyboards.admin_keyboards import (
    admin_main_menu,
    client_profile_for_adm,
)
from bot.keyboards.users_keyboards import profile_kb, reg_kb
from bot.utils.validators import check_user_is_admin, check_user_is_none

router = Router(name=__name__)


@router.message(CommandStart(deep_link=True))
async def decode_qr(
    message: Message, command: CommandObject,
    state: FSMContext, session: AsyncSession
):
    if await check_user_is_admin(
        tg_id=message.from_user.id, session=session
    ) and command.args is not None:
        await message.delete()
        payload = decode_payload(command.args)
        if not payload.isdigit():
            await message.answer('Произошла ошибка при сканировании.')
            return
        user = await users_crud.get_by_attribute(
            attr_name='tg_user_id', attr_value=int(payload), session=session
        )
        msg = await message.answer(
            CLIENT_BIO.format(
                last_name=user.last_name,
                first_name=user.first_name,
                birth_date=user.birth_date,
                phone_number=user.phone_number,
                balance=user.balance,
                note=user.note
            ),
            reply_markup=client_profile_for_adm
        )
        await state.update_data(
            phone_number=user.phone_number, msg_id=msg.message_id
        )


@router.message(CommandStart())
async def test(message: Message, session: AsyncSession):
    tg_id = message.from_user.id
    await message.delete()

    if await check_user_is_none(tg_id=tg_id, session=session):
        await message.answer(
            WELCOME_REG_MESSAGE,
            reply_markup=reg_kb,
        )
    elif await check_user_is_admin(tg_id=tg_id, session=session):
        await message.answer(
            WELCOME_ADMIN_MESSAGE,
            reply_markup=admin_main_menu,
        )
    else:
        await message.answer(
            PROFILE_MESSAGE_WITH_INLINE,
            reply_markup=profile_kb
        )
