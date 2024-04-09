from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.core.constants import (PROFILE_MESSAGE_WITH_INLINE, WELCOME_MESSAGE,
                                WELCOME_REG_MESSAGE)
from bot.keyboards.users_keyboards import profile_kb, reg_kb
from bot.utils.validators import check_user_from_db

router = Router(name=__name__)


@router.message(CommandStart())
async def test(message: Message, session: AsyncSession):
    tg_id = message.from_user.id
    await message.answer(WELCOME_MESSAGE)
    if await check_user_from_db(tg_id=tg_id, session=session):
        await message.answer(
            WELCOME_REG_MESSAGE,
            reply_markup=reg_kb,
        )
    else:
        await message.answer(
            PROFILE_MESSAGE_WITH_INLINE,
            reply_markup=profile_kb
        )
