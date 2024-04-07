from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards.users_keyboards import fsm_kb
from bot.utils.validators import check_user_from_db

router = Router(name=__name__)


@router.message(CommandStart())
async def test(message: Message, session: AsyncSession):
    tg_id = message.from_user.id
    await message.answer('Привет')
    if await check_user_from_db(tg_id=tg_id,session=session):
        await message.answer(
            'Для использования бота необходима регистрация',
            reply_markup=fsm_kb
        )

