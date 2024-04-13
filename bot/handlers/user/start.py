from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.core.constants import (PROFILE_MESSAGE_WITH_INLINE, WELCOME_MESSAGE,
                                WELCOME_REG_MESSAGE, WELCOME_ADMIN_MESSAGE)
from bot.core.test_base import test_base
from bot.keyboards.users_keyboards import profile_kb, reg_kb
from bot.keyboards.admin_keyboards import admin_main_menu
from bot.utils.validators import check_user_exists, check_user_is_admin

router = Router(name=__name__)


@router.message(CommandStart())
async def test(message: Message, session: AsyncSession):
    tg_id = message.from_user.id
    # FIXME
    #await test_base(session=session)
    
    if await check_user_exists(tg_id=tg_id, session=session):
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
