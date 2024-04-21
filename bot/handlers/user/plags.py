from datetime import datetime
from aiogram.fsm.context import FSMContext

from aiogram import Bot, F, Router
from aiogram.enums import ParseMode
from aiogram.types import BufferedInputFile, CallbackQuery
from aiogram.utils.deep_linking import create_start_link
from sqlalchemy.ext.asyncio import AsyncSession

from bot.core.constants import PROFILE_MESSAGE_WITH_INLINE
from bot.db.crud.users import users_crud
from bot.keyboards.users_keyboards import (
    back_menu_kb, profile_kb,
)
from bot.utils.qr_code import generate_qrcode

router = Router(name=__name__)


@router.callback_query()
async def plugs(
    callback: CallbackQuery,
    session: AsyncSession,
    state: FSMContext
):
    
    await callback.bot.send_sticker(
        chat_id=callback.from_user.id,
        sticker='CAACAgIAAxkBAAEE5ApmJWuVg0DS5KY29UTbBOHOKFzqLAAChhQAAmKy8EsG14-Zws0O-TQE'
        )