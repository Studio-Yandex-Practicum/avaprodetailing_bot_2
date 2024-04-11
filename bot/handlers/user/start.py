from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from bot.core.test_base import test_base

from bot.keyboards.users_keyboards import fsm_kb

router = Router(name=__name__)


@router.message(CommandStart())
async def test(message: Message, session: AsyncSession):
    await message.answer('Привет')
    # ОБЯЗАТЕЛЬНО СНЕСТИ!!!!!!!!!
    await test_base(session=session)
    await message.answer(
        'Для использования бота необходима регистрация',
        reply_markup=fsm_kb
    )

