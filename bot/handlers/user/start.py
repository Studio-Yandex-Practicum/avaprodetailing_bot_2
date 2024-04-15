from aiogram import Router, Bot
from aiogram.types import BufferedInputFile
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message
from aiogram.utils.deep_linking import create_start_link
from aiogram.utils.payload import decode_payload
from sqlalchemy.ext.asyncio import AsyncSession

from bot.core.constants import (
    PROFILE_MESSAGE_WITH_INLINE, WELCOME_MESSAGE,
    WELCOME_REG_MESSAGE, WELCOME_ADMIN_MESSAGE,
)
from bot.core.test_base import test_base
from bot.keyboards.users_keyboards import profile_kb, reg_kb
from bot.keyboards.admin_keyboards import admin_main_menu
from bot.utils.qr_code import generate_qrcode
from bot.utils.validators import check_user_is_none, check_user_is_admin

router = Router(name=__name__)


@router.message(Command('qrcode'))
async def referral(message: Message, bot: Bot):
    link = await create_start_link(bot, str(message.from_user.id), encode=True)

    qrcode = generate_qrcode(link)
    if qrcode is None:
        await message.answer('Произошла ошибка.\nПопробуйте позже')
        return
    await message.answer_photo(
        photo=BufferedInputFile(qrcode, 'qrcode.png'),
    )


@router.message(CommandStart(deep_link=True))
async def decode_qr(message: Message, command: CommandObject):
    await message.delete()
    # TODO: валидация аргументов
    if command.args is not None:
        payload = decode_payload(command.args)
        await message.answer(f"Профиль пользователя {payload}")


@router.message(CommandStart())
async def test(message: Message, session: AsyncSession):
    tg_id = message.from_user.id
    # FIXME
    # await test_base(session=session)

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
