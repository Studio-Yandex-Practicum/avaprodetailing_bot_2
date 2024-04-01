from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from .keyboard_test import reg_kb, fsm_kb

router = Router(name=__name__)


@router.message(CommandStart())
async def test(message: Message, state: FSMContext, session: AsyncSession):
    await message.answer(
        'Для использования бота необходима регистрация',
        reply_markup=fsm_kb
    )

