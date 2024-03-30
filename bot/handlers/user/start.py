from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

router = Router(name=__name__)


@router.message(CommandStart())
async def test(message: Message, state: FSMContext, session: AsyncSession):
    await message.answer('Alive')
