from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from keyboards.users_keyboards import fsm_kb, reg_kb
from sqlalchemy.ext.asyncio import AsyncSession
from utils.validators import user_check_before_reg

router = Router(name=__name__)


@router.message(CommandStart())
async def test(message: Message, state: FSMContext, session: AsyncSession):
    await message.answer('Привет')
    user_id = message.from_user.id
    if await user_check_before_reg(tg_user_id=user_id,session=session):
        await message.answer(
            'Для использования бота необходима регистрация',
            reply_markup=fsm_kb
        )

