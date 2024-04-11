from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models.users import User
from bot.states.payment_states import PaymentProcess

router = Router(name=__name__)

@router.callback_query(F.data == "Pay identification.")
async def pay_command(callback: CallbackQuery, session: AsyncSession):
    pass
